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

class SindonewsSpider(scrapy.Spider):
    name="sindonews"
    allowed_domains=["sindonews.com"]
    start_urls=(
        'http://metro.sindonews.com/topic/7282/pilgub-dki/',
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
        spider = super(SindonewsSpider, cls).from_crawler(crawler,
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

        for article in response.css('li > div.breaking-title'):
            # http://metro.sindonews.com/read/1146316/171/penyidik-bareskrim-mulai-dalami-video-dugaan-penistaan-agama-1476179831
            url = article.css('a::attr(href)').extract()[0]
            # Example 'Kamis, 13 Oktober 2016 - 11:18 WIB'
            date_time_str = article.css('p::text').extract()[0]

            # Parse date information
            try:
                # Example '13 Oktober 2016 - 11:18'
                date_time_str = date_time_str.split(',')[1].strip()[:-4]
                date_time_str = ' '.join([_(w) for w in date_time_str.split(' ')])
                self.logger.info('info_time: {}'.format(date_time_str))
                published_at = wib_to_utc(datetime.strptime(date_time_str, '%d %B %Y - %H:%M'))
            except Exception as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            if self.media['last_scraped_at'] >= published_at:
                is_scraped = True
                break

            # For each url we create new scrapy request
            yield scrapy.Request(url, callback=self.parse_news)

        if is_scraped:
            self.logger.info('Media have no update')
            return

        
        for next_button in response.css('.mpaging > ul > li'):
            if len(next_button.css('a:not(.active) > .fa-angle-right')) > 0:
              next_page = next_button.css('a::attr(href)').extract()[0]
              next_page_url = response.urljoin(next_page)
              yield scrapy.Request(next_page_url, callback=self.parse)
              break

    # Collect news item
    def parse_news(self, response):
        title = response.css('h1[itemprop="headline"]::text').extract()[0]
        author_name = response.css('a[rel="author"] > span::text').extract()[0]
        raw_content = response.css('.content').extract()[0]

        if not (title and author_name and raw_content):
            return

        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('title', title)
        loader.add_value('author_name', author_name)
        loader.add_value('raw_content', raw_content)

        # Parse date information
        try:
            # Example: Selasa,  6 Oktober 2015 - 05:23 WIB
            date_time_str = response.css('article > div.time::text').extract()[0]
            date_time_str = date_time_str.split(',')[1].strip()[:-4]
            date_time_str = ' '.join([_(w) for w in date_time_str.split(' ')])
            self.logger.info('parse_date: parse_news: date_str: %s', date_time_str)
            published_at = wib_to_utc(datetime.strptime(date_time_str, '%d %B %Y - %H:%M'))
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: %s' % e)

        # Move scraped news to pipeline
        return loader.load_item()
