# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.util.month import sanitize
from rojak_pantau.spiders.base import BaseSpider

import re

class NusanewsSpider(BaseSpider):
    name = "nusanews"
    allowed_domains = ["nusanews.co"]
    start_urls = [
            'http://www.nusanews.co/search/label/Pilkada?m=1'
    ]

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        is_no_update = False

        # Get list of news from the current page
        articles = response.css('article > div > div.post-content')

        if not articles:
            raise CloseSpider('article not found')
        for article in articles:
            # Close the spider if we don't find the list of urls
            url_selectors = article.css('a.timestamp-link::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example 'Sabtu, November 19, 2016'
            date_selectors = article.css('a.timestamp-link > abbr::text')
            if not date_selectors:
                raise CloseSpider('date_selectors not found')

            # Parse date information
            try:
                date = date_selectors.extract()[0].split(' ')
                # Sanitize month - Indo month to Eng month
                # Example: Nov 19 2016
                date[1] = sanitize(date[1])
                published_at_wib = datetime.strptime(' '.join(date[1:]),
                    '%b %d, %Y')
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
        if len(articles) > 0:
            try:
                yield Request('http://www.nusanews.co/search/label/Pilkada?updated-max=' +
                        str(published_at_wib).replace(' ','T') + '%2B07:00&max-results=20', callback=self.parse)
            except Exception as e:
                pass

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        # Required: title, raw_content, published_at
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title_selectors = response.css('article > h1 > a::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title.strip())

        # Parse date information
        # Example: 15 November, 2016
        date_selectors = response.css('a.timestamp-link > abbr::text')

        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()

        try:
            date = date_selectors.extract()[0].strip().split(' ')
            # Sanitize month
            date[1] = sanitize(date[1])
            published_at_wib = datetime.strptime(' '.join(date[1:]), '%b %d, %Y')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        # Extract the content using XPath instead of CSS selector
        # We get the XPath from chrome developer tools (copy XPath)
        # or equivalent tools from other browser
        xpath_query = """
            //div[@class="post-body entry-content"]/div/node()
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
        raw_content = ' '.join([w.encode('ascii', 'ignore').strip() for w in raw_content])
        raw_content = re.sub(r'<a.*?>(.*?)</a>', r'\1', raw_content.strip())
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
