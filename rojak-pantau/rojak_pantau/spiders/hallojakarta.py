# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.util.month import sanitize
from rojak_pantau.spiders.base import BaseSpider

class HalloJakartaSpider(BaseSpider):
    name = "hallojakarta"
    allowed_domains = ["hallojakarta.com"]
    start_urls = [
            'http://hallojakarta.com/category/news/politik'
    ]

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        is_no_update = False

        # Get list of news from the current page
        articles = response.css('article')
        if not articles:
            raise CloseSpider('article not found')
        for article in articles:
            # Close the spider if we don't find the list of urls
            url_selectors = article.css('a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example: 'Monday, 24/11/2016 | 13:54'
            date_selectors = article.css('time::text')
            if not date_selectors:
                raise CloseSpider('date_selectors not found')

            # Parse date information
            try:
                date = date_selectors.extract()[0].split(' ')
                published_at_wib = datetime.strptime(' '.join(date[1:]), '%d/%m/%Y | %H:%M')
            except ValueError as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break

            # For each url we create new scrapy request
            yield Request(url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        # try getting next page
        try:
            next_page_url = response.css('div.pagination > a.next::attr(href)').extract()[0]

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

        title_selectors = response.css('h1 > span.h-title::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title.strip())

        # Parse date information
        # Example: 15 November, 2016
        date_selectors = response.css('article.single-content > div.meta > span.time > time::text')

        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()

        try:
            date = date_selectors.extract()[0].split(' ')
            published_at_wib = datetime.strptime(' '.join(date[1:]), '%d/%m/%Y | %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        # no author name
        loader.add_value('author_name', '')

        # Extract the content using XPath instead of CSS selector
        # We get the XPath from chrome developer tools (copy XPath)
        # or equivalent tools from other browser
        xpath_query = """
            //article/div[@class="the-content post-content clearfix"]/node()
                [not(
                    descendant-or-self::comment()|
                    descendant-or-self::style|
                    descendant-or-self::script|
                    descendant-or-self::div|
                    descendant-or-self::span|
                    descendant-or-self::img|
                    descendant-or-self::table|
                    descendant-or-self::iframe
                )]
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
