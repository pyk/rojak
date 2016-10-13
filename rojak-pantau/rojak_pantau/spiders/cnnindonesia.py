# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.loader import ItemLoader

from rojak_pantau.items import News
from rojak_pantau.i18n import _
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
        is_scraped = False

        # Collect list of news from current page
        # Note: no next page button on cnnindonesia, all is loaded here
        for article in response.css('a.list_kontribusi'):
            url = article.css('a::attr(href)').extract()[0]
            # Example: Jumat, 23/09/2016 21:17
            info = article.css('div.text > div > span.tanggal::text').extract()[0]

            # Parse date information
            try:
                # Example: 23/09/2016 21:17
                info_time = info.split(',')[1].strip()
                self.logger.info('info_time: {}'.format(info_time))
                published_at = wib_to_utc(
                    datetime.strptime(info_time, '%d/%m/%Y %H:%M'))
            except Exception as e:
                raise CloseSpider('cannot_parse_date: {}'.format(e))

            if self.media['last_scraped_at'] >= published_at:
                is_scraped = True
                break
            # For each url we create new scrapy Request
            yield Request(url, callback=self.parse_news)

        if is_scraped:
            self.logger.info('Media have no update')
            return

    def parse_news(self, response):
        self.logger.info('parse_news: {}'.format(response))

        # Init item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title = response.css('div.detail_text > h1::text').extract()[0]
        author_name = response.css('div.author > strong::text').extract()[0]
        # Example: Senin, 10/10/2016 05:12
        date_str = response.css('div.date::text').extract()[0]
        # Extract raw html, not the text
        raw_content = response.css('div.detail_text').extract()[0]

        # Parse date information
        try:
            # Example: 10/10/2016 05:12
            date_str = date_str.split(',')[1].strip()
            self.logger.info('parse_date: parse_news: date_str: {}'.format(date_str))
            published_at = wib_to_utc(
                datetime.strptime(date_str, '%d/%m/%Y %H:%M'))
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: {}'.format(e))

        loader.add_value('title', title)
        loader.add_value('author_name', author_name)
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
