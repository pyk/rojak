# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.loader import ItemLoader

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

class CnnindonesiaSpider(BaseSpider):
    name = "cnnindonesia"
    allowed_domains = ["cnnindonesia.com"]
    start_urls = (
        'http://www.cnnindonesia.com/politik/focus/genderang-pilkada-jakarta-3335/berita',
        'http://www.cnnindonesia.com/politik/focus/berebut-suara-warga-jakarta-3338/berita',
        'http://www.cnnindonesia.com/politik/focus/janji-manis-calon-gubernur-3348/berita'
    )

    def parse(self, response):
        self.logger.info('parse: {}'.format(response))
        is_no_update = False

        # Collect list of news from current page
        # Note: no next page button on cnnindonesia, all is loaded here
        article_selectors = response.css('a.list_kontribusi');
        if not article_selectors:
            raise CloseSpider('article_selectors not found')

        for article in article_selectors:
            url_selectors = article.css('a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example: Jumat, 23/09/2016 21:17
            info_selectors = article.css('div.text > div > span.tanggal::text')
            if not info_selectors:
                raise CloseSpider('info_selectors not found')
            info = info_selectors.extract()[0]
            info_time = info.split(',')[1].strip()

            # Parse date information
            try:
                # Example: 23/09/2016 21:17
                published_at_wib = datetime.strptime(info_time, '%d/%m/%Y %H:%M')
            except ValueError as err:
                raise CloseSpider('cannot_parse_date: {}'.format(err))
            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break
            # For each url we create new scrapy Request
            yield Request(url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

    def parse_news(self, response):
        self.logger.info('parse_news: {}'.format(response))

        # Init item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title_selectors = response.css('div.detail_text > h1::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title)

        # Extract raw html, not the text
        # Using Xpath instead of CSS selector to eliminate useless children
        xpath_query = """
            //div[@class="detail_text"]/node()
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

        # Example: Senin, 10/10/2016 05:12
        date_selectors = response.css('div.date::text')
        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        date_str = date_selectors.extract()[0]
        # Example: 10/10/2016 05:12
        date_str = date_str.split(',')[1].strip()
        # Parse date information
        try:
            published_at_wib = datetime.strptime(date_str, '%d/%m/%Y %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()
        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        author_name_selectors = response.css('div.author > strong::text')
        if not author_name_selectors:
            loader.add_value('author_name', '')
        else:
            author_name = author_name_selectors.extract()[0]
            loader.add_value('author_name', author_name)

        # Move scraped news to pipeline
        return loader.load_item()
