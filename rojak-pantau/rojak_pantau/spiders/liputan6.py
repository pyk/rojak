# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from rojak_pantau.items import News
from rojak_pantau.i18n import _
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

class Liputan6Spider(BaseSpider):
    name = "liputan6"
    allowed_domains = ["liputan6.com"]
    start_urls = (
        'http://m.liputan6.com/tag/pilkada-dki-jakarta-2017',
        'http://m.liputan6.com/tag/pilkada-dki-2017',
    )

    # Only the last 60 pages can be crawled, liputan6 API is not understandable
    def parse(self, response):
        self.logger.info('parse: %s' % response)
        is_no_update = False

        # Get list of news from the current page
        articles = response.css('div.article-snippet__info')
        if not articles:
            raise CloseSpider('article not found')
        for article in articles:
            # Close the spider if we don't find the list of urls
            url_selectors = article.css('a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            info_selectors = article.css('div.article-snippet__date')
            info_selectors = info_selectors.css('.timeago::text')
            if not info_selectors:
                raise CloseSpider('info_selectors not found')
            # Example '13 Okt 2016 16:10'
            info_time = info_selectors.extract()[0]
            # Example '13 Oct 2016 16:10'
            info_time = ' '.join([_(w) for w in info_time.split(' ')])

            # Parse date information
            try:
                published_at_wib = datetime.strptime(info_time,
                    '%d %b %Y %H:%M')
            except ValueError as e:
                raise CloseSpider('cannot_parse_date: {}'.format(e))

            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break

            # For each url we create new scrapy Request
            yield Request(url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

    # TODO: Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        # Required: title, raw_content, published_at
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)
        title_selectors = response.css('h1.article-header__title::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title)

        # Extract the content using XPath instead of CSS selector
        xpath_query = """
            //div[@class="article-raw-content"]/node()
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

        # Parse date information
        # Example: ' pada 18 Okt 2016, 08:33 WIB'
        date_selectors = response.css('span.article-header__datetime::text')
        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()

        date_str = date_selectors.extract()[0].strip()
        # Example: '18 Oct 2016, 08:33'
        date_str = ' '.join([_(w) for w in date_str.split(' ')[1:-1]])
        try:
            published_at_wib = datetime.strptime(date_str, '%d %b %Y, %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        author_name_selectors = response.css('a.article-header__author-link::text')
        if not author_name_selectors:
            loader.add_value('author_name', '')
        else:
            author_name = author_name_selectors.extract()[0]
            loader.add_value('author_name', author_name)

        # Move scraped news to pipeline
        return loader.load_item()
