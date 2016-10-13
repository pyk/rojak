# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse

from rojak_pantau.items import News
from rojak_pantau.i18n import _
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

NEWS_LIMIT = 600
PARAMS = 'taglistdetail.php?catName=pilgub-dki-2017&p=1&limit={}'.format(NEWS_LIMIT)

class BeritasatuSpider(BaseSpider):
    name = "beritasatu"
    allowed_domains = ["beritasatu.com"]
    start_urls = [
        # Consume API directly, this returns JSON response
        'http://m.beritasatu.com/static/json/mobile/{}'.format(PARAMS)
    ]

    def parse(self, response):
        self.logger.info('parse: {}'.format(response))
        is_scraped = False

        # beritasatu response is HTML snippet wrapped in a JSON response
        data = json.loads(response.body_as_unicode())
        response = HtmlResponse(url=response.url, body=data['content'].encode('utf-8'))

        # Note: no next page button on beritasatu, all is loaded here
        # adjust how many links to extract from NEWS_LIMIT const
        for article in response.css('div.headfi'):
            url = 'http://www.beritasatu.com{}'.format(
                article.css('h4 > a::attr(href)').extract()[0])
            # Example: Kamis, 06 Oktober 2016 | 10:11 -
            info = article.css('div.ptime > span.datep::text').extract()[0]

            # Parse date information
            try:
                # Example: 06 October 2016 10:11
                info_time = re.split('[\s,|-]', info)
                info_time = ' '.join([_(s) for s in info_time[1:] if s])
                self.logger.info('info_time: {}'.format(info_time))
                published_at = wib_to_utc(
                    datetime.strptime(info_time, '%d %B %Y %H:%M'))
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

        title = response.css('div.content-detail > h4::text').extract()[0]
        author_name = response.css('div.content-detail > p::text').extract()[0]
        author_name = author_name.split('/')[0]
        # Example: Selasa, 11 Oktober 2016 | 10:48
        date_str = response.css('div.date::text').extract()[0]
        # Extract raw html, not the text
        raw_content = response.css('div.content-body').extract()[0]

        # Parse date information
        try:
            # Example: 11 October 2016 10:48
            date_str = re.split('[\s,|-]', date_str)
            date_str = ' '.join([_(s) for s in date_str[1:] if s])
            self.logger.info('parse_date: parse_news: date_str: {}'.format(date_str))
            published_at = wib_to_utc(
                datetime.strptime(date_str, '%d %B %Y %H:%M'))
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: {}'.format(e))

        loader.add_value('title', title)
        loader.add_value('author_name', author_name)
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
