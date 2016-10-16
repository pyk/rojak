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
        is_no_update = False

        # Collect list of news from current page
        articles = json.loads(response.body)['response']
        for article in articles:
            # Example: 2016-10-12 15:16:04
            date_time_str = article['news_date_publish']

            # Parse date information
            try:
                published_at_wib = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            except Exception as e:
                raise CloseSpider('cannot_parse_date: {}'.format(e))
            published_at = wib_to_utc(published_at_wib)

            if (self.media['last_scraped_at'] >= published_at):
                is_no_update = True
                break;

            for sub_article in article['news_content']:
                yield self.parse_news(article, sub_article)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        # Collect news on next page
        if len(articles) > 0:
            # Example: 'http://api.merdeka.com/mobile/gettag/pilgub-dki/0/20/L9pTAoWB269T&-E/'
            next_page_url = response.url.split('/')
            next_page_url[-4] = str(int(next_page_url[-4]) + 20)
            next_page_url = '/'.join(next_page_url)
            yield Request(next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, article, sub_article):
        self.logger.info('parse_news: %s' % article)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News())

        # Example: https://m.merdeka.com/tag/p/pilgub-dki/politik/nachrowi-pastikan-agus-sylvi-tak-cuma-incar-suara-santri-ulama.html
        if not sub_article['news_url']:
            return loader.load_item()
        url = 'https://www.merdeka.com' + sub_article['news_url']
        loader.add_value('url', url)

        if not article['news_title']:
            return loader.load_item()
        loader.add_value('title', article['news_title'])

        if not article['news_reporter']:
            loader.add_value('author_name', '')
        else:
            loader.add_value('author_name', article['news_reporter'])

        if not sub_article['news_description']:
            return loader.load_item()
        loader.add_value('raw_content', sub_article['news_description'])

        # Parse date information
        date_time_str = article['news_date_publish']
        try:
            # Example: 2016-10-12 15:16:04
            published_at_wib = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        # Move scraped news to pipeline
        return loader.load_item()
