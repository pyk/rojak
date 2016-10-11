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


class CnnindonesiaSpider(Spider):
    name = "cnnindonesia"
    allowed_domains = ["cnnindonesia.com"]
    start_urls = (
        'http://www.cnnindonesia.com/politik/focus/genderang-pilkada-jakarta-3335/berita',

    )
    # TODO: add 2 more URLs
    # 'http://www.cnnindonesia.com/politik/focus/berebut-suara-warga-jakarta-3338/berita',
    # 'http://www.cnnindonesia.com/politik/focus/janji-manis-calon-gubernur-3348/berita'

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
        spider = super(CnnindonesiaSpider, cls).from_crawler(crawler,
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
