# -*- coding: utf-8 -*-
import scrapy
import MySQLdb as mysql
import os
from datetime import datetime
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy import signals
from rojak_pantau.items import News
from scrapy.loader import ItemLoader
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

sql_update_media = '''
UPDATE `media` SET last_scraped_at=%s WHERE name=%s;
'''

# TODO: understanding di scheduler works not only once
# TODO: save state last_scraped_at
class DetikcomSpider(scrapy.Spider):
    name = "detikcom"
    allowed_domains = ["detik.com"]
    start_urls = (
        'http://m.detik.com/news/indeksfokus/67/jakarta-memilih/1',
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
        spider = super(DetikcomSpider, cls).from_crawler(crawler,
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
                self.cursor.execute(sql_update_media, [datetime.now(),
                    self.name])
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
        self.logger.info('parse: %s' % response)
        is_scraped = False

        # Get list of news from the current page
        for article in response.css('article'):
            url = article.css('a::attr(href)').extract()[0]
            # Example 'detikNews | Sabtu 08 Oct 2016, 14:54 WIB'
            info = article.css('a > .text > span.info::text').extract()[0]

            # Parse date information
            try:
                # Example 'Sabtu 08 Oct 2016, 14:54 WIB'
                info_time = info.split('|')[1].strip()
                # Example '08 Oct 2016, 14:54'
                info_time = ' '.join(info_time.split(' ')[1:5])
                self.logger.info('info_time: %s', info_time)
                published_at = datetime.strptime(info_time,
                    '%d %b %Y, %H:%M')
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

        if response.css('a.btn_more'):
            next_page = response.css('a.btn_more::attr(href)')[0].extract()
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
        elif response.css('div.pag-nextprev > a'):
            next_page = response.css('div.pag-nextprev > a::attr(href)')[1].extract()
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)
        title = response.css('div.detail_area > h1.jdl::text').extract()[0]
        loader.add_value('title', title)
        author_name = response.css('div.author > strong::text').extract()[0]
        loader.add_value('author_name', author_name)
        raw_content = response.css('article > div.text_detail::text').extract()
        raw_content = ' '.join(raw_content)
        loader.add_value('raw_content', raw_content)

        # Parse date information
        try:
            # Example: Kamis 15 Sep 2016, 18:33 WIB
            date_str = response.css('div.detail_area > div.date::text').extract()[0]
            # Example: '15 Sep 2016, 18:33'
            date_str = ' '.join(date_str.split(' ')[1:5])
            self.logger.info('parse_date: parse_news: date_str: %s', date_str)
            published_at = datetime.strptime(date_str,
                '%d %b %Y, %H:%M')
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: %s' % e)

        # Move scraped news to pipeline
        return loader.load_item()

