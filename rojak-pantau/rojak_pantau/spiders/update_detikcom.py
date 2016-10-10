# -*- coding: utf-8 -*-
# Spider for update existing content on the database
import scrapy
import MySQLdb as mysql
import os
from datetime import datetime
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy import signals
from slacker import Slacker

ROJAK_DB_HOST = os.getenv('ROJAK_DB_HOST', 'localhost')
ROJAK_DB_PORT = int(os.getenv('ROJAK_DB_PORT', 3306))
ROJAK_DB_USER = os.getenv('ROJAK_DB_USER', 'root')
ROJAK_DB_PASS = os.getenv('ROJAK_DB_PASS', 'rojak')
ROJAK_DB_NAME = os.getenv('ROJAK_DB_NAME', 'rojak_database')
ROJAK_SLACK_TOKEN = os.getenv('ROJAK_SLACK_TOKEN', '')

sql_get_media = '''
SELECT id,last_scraped_at FROM media WHERE name=%s;
'''

sql_update_news = '''
UPDATE `news` SET title=%s, author_name=%s, raw_content=%s,
    published_at=%s
WHERE url=%s;
'''

sql_get_urls = '''
SELECT `url` FROM news WHERE media_id=%s;
'''

class UpdateDetikcomSpider(scrapy.Spider):
    name = "update_detikcom"
    allowed_domains = ["detik.com"]

    # Initialize database connection then retrieve media ID and
    # last_scraped_at information
    def __init__(self):
        # Open database connection
        self.db = mysql.connect(host=ROJAK_DB_HOST, port=ROJAK_DB_PORT,
            user=ROJAK_DB_USER, passwd=ROJAK_DB_PASS, db=ROJAK_DB_NAME)
        self.cursor = self.db.cursor()
        self.cursor_urls = self.db.cursor()

        # Using UTF-8 Encoding
        self.db.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

        self.media = {}
        self.media['name'] = 'detikcom'
        try:
            # Get media information from the database
            self.logger.info('Fetching media information')
            self.cursor.execute(sql_get_media, [self.media['name']])
            row = self.cursor.fetchone()
            self.media['id'] = row[0]
            self.media['last_scraped_at'] = row[1]
        except mysql.Error as err:
            self.logger.error('Unable to fetch media data: %s', err)
            raise NotConfigured('Unable to fetch media data: %s' % err)

        if ROJAK_SLACK_TOKEN != '':
            self.is_slack = True
            self.slack = Slacker(ROJAK_SLACK_TOKEN)
        else:
            self.is_slack = False
            self.logger.info('Post error to #rojak-pantau-errors is disabled')

        # We execute the cursor here and we fetch one by one
        self.cursor_urls.execute(sql_get_urls, [self.media['id']])

    # Fetch the first url and create new request
    def start_requests(self):
        url = self.cursor_urls.fetchone()[0]
        yield scrapy.Request(url=url, callback=self.update_news)

    # Capture the signal spider_opened and spider_closed
    # https://doc.scrapy.org/en/latest/topics/signals.html
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(UpdateDetikcomSpider, cls).from_crawler(crawler,
                *args, **kwargs)
        crawler.signals.connect(spider.spider_opened,
                signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed,
                signal=signals.spider_closed)
        return spider

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s', spider.name)

    def spider_closed(self, spider, reason):
        spider.logger.info('Spider closed: %s %s', spider.name, reason)

    # Parse news and update to the database
    def update_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # extract news title, published_at, author, content, url
        title = response.css('div.detail_area > h1.jdl::text').extract()[0]
        author_name = response.css('div.author > strong::text').extract()[0]
        raw_content = response.css('article > div.text_detail').extract()[0]

        # Parse date information
        try:
            # Example: Kamis 15 Sep 2016, 18:33 WIB
            date_str = response.css('div.detail_area > div.date::text').extract()[0]
            # Example: '15 Sep 2016, 18:33'
            date_str = ' '.join(date_str.split(' ')[1:5])
            self.logger.info('parse_date: parse_news: date_str: %s', date_str)
            published_at = datetime.strptime(date_str,
                '%d %b %Y, %H:%M')
        except Exception as e:
            raise CloseSpider('cannot_parse_date: %s' % e)

        # Update the news
        try:
            # Get media information from the database
            self.cursor.execute(sql_update_news, [title, author_name,
                raw_content, published_at, response.url])
            self.db.commit()
        except mysql.Error as err:
            self.db.rollback()
            msg = 'Unable to update news: %s' % err
            raise CloseSpider(msg)

        url = self.cursor_urls.fetchone()[0]
        yield scrapy.Request(url=url, callback=self.update_news)

