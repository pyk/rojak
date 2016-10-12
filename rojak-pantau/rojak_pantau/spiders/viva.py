# -*- coding: utf-8 -*-
import os
import MySQLdb as mysql
from datetime import datetime
from scrapy import Spider, Request, signals
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.loader import ItemLoader
from slacker import Slacker

from rojak_pantau.items import News
from rojak_pantau.i18n import _
from rojak_pantau.util.wib_to_utc import wib_to_utc

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
UPDATE `media` SET last_scraped_at=%s WHERE name=%s;
'''


class VivaSpider(Spider):
    name = "viva"
    allowed_domains = ["viva.co.id"]
    start_urls = (
        'http://www.viva.co.id/tag/Pilkada-DKI-Jakarta-2017/1',
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
        spider = super(VivaSpider, cls).from_crawler(crawler,
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
        spider.logger.info('Spider closed: {} {}'.format(spider.name, reason))

        # update last_scraped_at if spider finished without error
        if reason == 'finished':
            try:
                self.logger.info('Updating media last_scraped_at information')
                self.cursor.execute(sql_update_media, [datetime.utcnow(),
                    self.name])
                self.db.commit()
                self.db.close()
            except mysql.Error as err:
                self.logger.error('Unable to update last_scraped_at: {}'.format(err))
                self.db.rollback()
                self.db.close()

        else:
            if self.is_slack:
                # Send error to slack
                error_msg = '{}: Unable to update last_scraped_at: {}'.format(
                    spider.name, err)
                self.slack.chat.post_message('#rojak-pantau-errors',
                    error_msg, as_user=True)
