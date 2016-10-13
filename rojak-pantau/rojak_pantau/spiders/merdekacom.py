# -*- coding: utf-8 -*-
import json

from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader

from datetime import datetime

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.i18n import _
from rojak_pantau.spiders.base import BaseSpider

class MerdekacomSpider(BaseSpider):
    name="merdeka.com"
    allowed_domains=["merdeka.com"]
    start_urls=(
        'http://api.merdeka.com/mobile/gettag/pilgub-dki/0/20/L9pTAoWB269T&-E/',
    )

    def parse(self, response):
        self.logger.info('parse: {}'.format(response))
        is_scraped = False

        # Collect list of news from current page
        articles = json.loads(response.body)['response']
        for article in articles:
            # Example: 2016-10-12 15:16:04
            date_time_str = article['news_date_publish']

            # Parse date information
            try:
                self.logger.info('info_time: {}'.format(date_time_str))
                published_at = wib_to_utc(
                        datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S'))
            except Exception as e:
                raise CloseSpider('cannot_parse_date: {}'.format(e))

            if (self.media['last_scraped_at'] >= published_at):
                is_scraped = True
                break;

            for sub_article in article['news_content']:
                yield self.parse_news(article, sub_article)

        if is_scraped:
            self.logger.info('Media have no update')
            return

        # Collect news on next page
        if len(articles) > 0:
            'http://api.merdeka.com/mobile/gettag/pilgub-dki/0/20/L9pTAoWB269T&-E/',
            next_page_url = response.url.split('/')
            next_page_url[-4] = str(int(next_page_url[-4]) + 20)
            next_page_url = '/'.join(next_page_url)
            yield Request(next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, article, sub_article):
        if not (sub_article['news_url'] and article['news_title'] and article['news_reporter'] and sub_article['news_description'] and article['news_date_publish']):
            return

        self.logger.info('parse_news: %s' % article)

        # Example: https://m.merdeka.com/tag/p/pilgub-dki/politik/nachrowi-pastikan-agus-sylvi-tak-cuma-incar-suara-santri-ulama.html
        url = 'https://www.merdeka.com' + sub_article['news_url']

        # Initialize item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News())
        loader.add_value('url', url)
        loader.add_value('title', article['news_title'])
        loader.add_value('author_name', article['news_reporter'])
        loader.add_value('raw_content', sub_article['news_description'])

        # Parse date information
        try:
            # Example: 2016-10-12 15:16:04
            date_time_str = article['news_date_publish']
            self.logger.info('parse_date: parse_news: date_str: %s', date_time_str)
            published_at = wib_to_utc(
                        datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S'))
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: %s' % e)

        # Move scraped news to pipeline
        return loader.load_item()
