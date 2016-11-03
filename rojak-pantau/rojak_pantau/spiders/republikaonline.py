# -*- coding: utf-8 -*-
import re
from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.util.month import sanitize
from rojak_pantau.spiders.base import BaseSpider

class RepublikaOnlineSpider(BaseSpider):
    name = "republikaonline"
    allowed_domains = ["republika.co.id"]
    start_urls = [
            'http://www.republika.co.id/indeks/hot_topic/pilgub_dki'
    ]

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        is_no_update = False

        # Get list of news from the current page
        articles = response.css('div.wp-terhangat > div.item3')

        if not articles:
            raise CloseSpider('article not found')
        for article in articles:
            # Close the spider if we don't find the list of urls
            url_selectors = article.css('a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example 'Wednesday, 02 November 2016'
            date_selectors = article.css('span.date::text')
            if not date_selectors:
                raise CloseSpider('date_selectors not found')

            # Parse date information
            try:
                date = date_selectors.extract()[0].split(' ')
                # Sanitize month - Indo month to Eng month
                # Example: Wednesday, 02 Nov 2016
                date[2] = sanitize(date[2])
                published_at_wib = datetime.strptime(' '.join(date[1:]),
                    '%d %b %Y')
            except ValueError as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            published_at = wib_to_utc(published_at_wib)

            # if it's news from before 2015, drop them
            if self.media['last_scraped_at'] >= published_at or int(date[-1]) < 2015:
                is_no_update = True
                break

            # For each url we create new scrapy request
            yield Request(url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        # try getting next page
        try:
            next_page_url = response.css('nav > ul > li > a::attr(href)').extract()[-1]

            if next_page_url:
               yield Request(next_page_url, callback=self.parse)
        except:
            pass

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        # Required: title, raw_content, published_at
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title_selectors = response.css('div.wrap-head > h2 > a')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = ''.join(title_selectors[0].xpath('.//text()').extract())
        loader.add_value('title', title.strip())

        # Parse date information
        # Example: Rabu, 02 November 2016, 10:29 WIB
        date_selectors = response.css('div.wrap-head > span.date::text')

        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()

        try:
            date = date_selectors.extract()[0].strip().split(' ')
            # Sanitize month
            date[2] = sanitize(date[2])
            published_at_wib = datetime.strptime(' '.join(date[1:]), '%d %b %Y | %H:%M WIB')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        author_name_selectors = response.css('div.red::text')
        if not author_name_selectors:
            loader.add_value('author_name', '')
        else:
            authors = [author.strip() for author in author_name_selectors.extract()]
            # Only consider Red: as author
            # Example: ['Rep: Dadang Kurnia', 'Red: Bilal Ramadhan']
            author_names = [name[4:].strip() for name in filter(lambda a: a.count('Red:') > 0, authors)]
            loader.add_value('author_name', ','.join(author_names))

        # Extract the content using XPath instead of CSS selector
        # We get the XPath from chrome developer tools (copy XPath)
        # or equivalent tools from other browser
        xpath_query = """
            //article/div[@class="content-detail"]/p/node()
        """
        raw_content_selectors = response.xpath(xpath_query)
        if not raw_content_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        raw_content = raw_content_selectors.extract()
        raw_content = ' '.join([w.strip() for w in raw_content])
        raw_content = raw_content.strip()
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
