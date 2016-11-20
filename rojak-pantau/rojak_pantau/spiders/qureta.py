# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

class QuretaSpider(BaseSpider):
    name = "qureta"
    allowed_domains = ["qureta.com"]
    start_urls = ('http://www.qureta.com/topik/politik',)

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        is_no_update = False

        # Get list of news from the current page
        articles = response.css('div.view-front > div.view-content > div.views-row')

        if not articles:
            raise CloseSpider('article not found')
        for article in articles:
            # Close the spider if we don't find the list of urls
            url_selectors = article.css('span.field-content a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example '19 Oct 2016'
            info_selectors = article.css('span.field-content::text')
            if not info_selectors:
                raise CloseSpider('info_selectors not found')
            info_time = info_selectors.extract()[1].strip()

            # Parse date information
            try:
                published_at_wib = datetime.strptime(info_time, '%d %b %Y')
            except ValueError as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break

            # For each url we create new scrapy request
            yield Request('http://www.qureta.com' + url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        if response.css('li.next'):
            next_page_url = response.css('li.next > a::attr(href)')[0].extract()
            yield Request('http://www.qureta.com' + next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        # Required: title, raw_content, published_at
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title_selectors = response.css('div.field-name-title > div > div > h2::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title)

        # Parse date information
        # Example: 31 Oct 2016
        date_selectors = response.css('div.field-name-post-date > div > div::text')
        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()

        date_str = date_selectors.extract()[0]
        try:
            published_at_wib = datetime.strptime(date_str, '%d %b %Y')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        author_name_selectors = response.css('div.views-field-view-user > span > a::text')
        if not author_name_selectors:
            loader.add_value('author_name', '')
        else:
            author_name = author_name_selectors.extract()[0]
            loader.add_value('author_name', author_name.strip())

        # Extract the content using XPath instead of CSS selector
        # We get the XPath from chrome developer tools (copy XPath)
        # or equivalent tools from other browser
        xpath_query = """
            //div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]
                /div/div/node()
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
        loader.add_value('raw_content', raw_content.encode('ascii', 'ignore'))

        # Move scraped news to pipeline
        return loader.load_item()
