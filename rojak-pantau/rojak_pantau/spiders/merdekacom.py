# -*- coding: utf-8 -*-
import os
import json
import scrapy
import MySQLdb as mysql

from scrapy import signals, Request
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.loader import ItemLoader

from datetime import datetime
from slacker import Slacker

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.i18n import _

ROJAK_DB_HOST = os.getenv('ROJAK_DB_HOST', 'localhost')
ROJAK_DB_PORT = int(os.getenv('ROJAK_DB_PORT', 3306))
ROJAK_DB_USER = os.getenv('ROJAK_DB_USER', 'root')
ROJAK_DB_PASS = os.getenv('ROJAK_DB_PASS', 'rojak')
ROJAK_DB_NAME = os.getenv('ROJAK_DB_NAME', 'rojak_database')
ROJAK_SLACK_TOKEN = os.getenv('ROJAK_SLACK_TOKEN', '')

sql_get_media = '''
SELECT id,last_scraped_at FROM media WHERE name=%s;
'''

sql_update_media = '''
UPDATE `media` SET last_scraped_at=UTC_TIMESTAMP() WHERE name=%s;
'''

class MerdekacomSpider(scrapy.Spider):
    name="merdeka.com"
    allowed_domains=["merdeka.com"]
    start_urls=(
        'http://api.merdeka.com/mobile/gettag/pilgub-dki/0/20/L9pTAoWB269T&-E/',
    )

    # Initialize database connection then retrieve media ID and
    # last_scraped_at information
    def __init__(self):
        # Open database connection
        self.db = mysql.connect(host=ROJAK_DB_HOST, port=ROJAK_DB_PORT,
            user=ROJAK_DB_USER, passwd=ROJAK_DB_PASS, db=ROJAK_DB_NAME)
        self.cursor = self.db.cursor()

        self.media = {}
        try:
            # Get media information from the database
            self.logger.info('Fetching media information')
            self.cursor.execute(sql_get_media, [self.name])
            row = self.cursor.fetchone()
            self.media['id'] = row[0]
            self.media['last_scraped_at'] = row[1]
        except mysql.Error as err:
            self.logger.error('Unable to fetch media data: {}'.format(err))
            raise NotConfigured('Unable to fetch media data: {}'.format(err))

        if ROJAK_SLACK_TOKEN != '':
            self.is_slack = True
            self.slack = Slacker(ROJAK_SLACK_TOKEN)
        else:
            self.is_slack = False
            self.logger.info('Post error to #rojak-pantau-errors is disabled')

    # Capture the signal spider_opened and spider_closed
    # https://doc.scrapy.org/en/latest/topics/signals.html
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(MerdekacomSpider, cls).from_crawler(crawler,
                *args, **kwargs)
        crawler.signals.connect(spider.spider_opened,
                signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed,
                signal=signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        # Using UTF-8 Encoding
        self.db.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def spider_closed(self, spider, reason):
        spider.logger.info('Spider closed: %s %s', spider.name, reason)
        # if spider finished without error update last_scraped_at
        if reason == 'finished':
            try:
                self.logger.info('Updating media last_scraped_at information')
                self.cursor.execute(sql_update_media, [self.name])
                self.db.commit()
                self.db.close()
            except mysql.Error as err:
                self.logger.error('Unable to update last_scraped_at: %s', err)
                self.db.rollback()
                self.db.close()
                if self.is_slack:
                    error_msg = '{}: Unable to update last_scraped_at: {}'.format(
                        spider.name, err)
                    self.slack.chat.post_message('#rojak-pantau-errors', error_msg,
                        as_user=True)
        else:
            if self.is_slack:
                # Send error to slack
                error_msg = '{}: Spider fail because: {}'.format(
                    self.name, reason)
                self.slack.chat.post_message('#rojak-pantau-errors',
                        error_msg, as_user=True)

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
