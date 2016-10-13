# -*- coding: utf-8 -*-
import scrapy
import MySQLdb as mysql
import os
from datetime import datetime
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy import signals
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
UPDATE `media` SET last_scraped_at=UTC_TIMESTAMP() WHERE name=%s;
'''

class KompasComSpider(scrapy.Spider):
    name = "kompas"
    start_urls = [
        'http://lipsus.kompas.com/topikpilihanlist/3754/1/Pilkada.DKI.2017'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
    }

    # Initialize database connection then retrieve media ID and
    # last_scraped_at information
    def __init__(self):
        # Open database connection
        self.db = mysql.connect(host=ROJAK_DB_HOST, port=ROJAK_DB_PORT, user=ROJAK_DB_USER, passwd=ROJAK_DB_PASS, db=ROJAK_DB_NAME)
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
            self.logger.error('Unable to fetch media data: %s', err)
            raise NotConfigured('Unable to fetch media data: %s' % err)

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
        spider = super(KompasComSpider, cls).from_crawler(crawler,
            *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
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
                    error_msg = '{}: Unable to update last_scraped_at: {}'.format(spider.name, err)
                    self.slack.chat.post_message('#rojak-pantau-errors', error_msg, as_user=True)
        else:
            if self.is_slack:
                # Send error to slack
                error_msg = '{}: Spider fail because: {}'.format(self.name, reason)
                self.slack.chat.post_message('#rojak-pantau-errors', error_msg, as_user=True)   

    def parse(self, response):
        is_scraped = False

        for news in response.css("ul.clearfix > li > div.tleft"):
            url = news.css("div.tleft > h3 > a::attr(href)").extract()[0]
            raw_date = news.css("div.grey.small::text").extract()[0]

            # Parse date information
            try:
                published_at = self.convert_date(raw_date);
            except Exception as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            if self.media['last_scraped_at'] >= published_at:
                is_scraped = True
                break
            #For each url we create new scrapy request
            yield scrapy.Request(url=url, callback=self.parse_news)

        if is_scraped:
            self.logger.info('Media have no update')
            return
    
        next_pages = response.css("ul.paginasi.mt2 > li > a::attr(href)").extract()
        for next_url in next_pages:
            yield scrapy.Request(next_url, callback=self.parse)

    def convert_date(self, idn_date):
        # Example Rabu, 12 Oktober 2016 | 10:23 WIB
        info_time = idn_date.split(',')[1].strip().split('|');
        info_date = info_time[0].strip().split(' ');
        info_hours = info_time[1].strip().split(' ')[0].strip();
        day = info_date[0];
        month = _(info_date[1]);
        year = info_date[2];
        formatted_date = day+' '+month+' '+year+', ' + info_hours;
        return  wib_to_utc(datetime.strptime(formatted_date, '%d %B %Y, %H:%M'));

    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)
        
        title = ' '.join(response.css("div.kcm-read-top > h2::text").extract())
        author_name = ', '.join(response.css("span.pb_10::text").extract())
        raw_content = response.css("div.kcm-read-text > p").extract()
        raw_content = ' '.join(raw_content)
        date = response.css("div.kcm-date::text").extract()[0];

        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('title', title)
        loader.add_value('author_name', author_name)
        loader.add_value('raw_content', raw_content)
        loader.add_value('url', response.url)
        try:
            loader.add_value('published_at',self.convert_date(date))
        except Exception as e:
            raise CloseSpider('cannot_parse_date: %s' % e)
        
        return loader.load_item()
