# -*- coding: utf-8 -*-
import os
import re
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

class OkezoneSpider(scrapy.Spider):
    name="okezone"
    allowed_domains=["okezone.com"]
    start_urls=(
        'http://news.okezone.com/more_topic/25962/0',
    )

    # Some offset parameter in okezone has bug
    # Example: http://news.okezone.com/more_topic/25962/1180 can't be accessed
    # However, http://news.okezone.com/more_topic/25962/1185 is accessible
    # This spider will stop once it encounters 5 consecutive empty pages
    failed_count=0

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
        spider = super(OkezoneSpider, cls).from_crawler(crawler,
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
        articles = response.css('li.col-md-12')
        for article in articles:
            # Example: http://news.okezone.com/read/2016/10/12/338/1512347/marak-isu-sara-jelang-pilgub-begini-cara-mencegahnya
            url_selectors = article.css('h3 > a::attr(href)')

            if not url_selectors:
                raise CloseSpider('url_selectors not found')

            url_selectors = url_selectors.extract()[0]
            # Use Okezone Mobile App API
            # Example: http://services.okezone.com/android/mobile_topic/2016/10/12/338/1512347/marak-isu-sara-jelang-pilgub-begini-cara-mencegahnya
            url = 'http://services.okezone.com/android/apps_detail/' + '/'.join(url_selectors.split('/')[-6:])


            # Example: Rabu, 12 Oktober 2016 06:44 WIB
            date_time_str_selectors = article.css('time::text')

            if not date_time_str_selectors or len(date_time_str_selectors) < 2:
                raise CloseSpider('date_time_str_selectors not found')

            date_time_str = date_time_str_selectors.extract()[1].strip()

            # Parse date information
            try:
                # Example: 12 October 2016 06:44
                # Remove WIB and convert the date to International based
                date_time_str = date_time_str.split(',')[1].strip();
                date_time_str = ' '.join([_(w) for w in date_time_str[:-4].split(' ')])
                self.logger.info('info_time: {}'.format(date_time_str))
                published_at = wib_to_utc(
                    datetime.strptime(date_time_str, '%d %B %Y %H:%M'))
            except Exception as e:
                raise CloseSpider('cannot_parse_date: {}'.format(e))

            if (self.media['last_scraped_at'] >= published_at):
                is_scraped = True
                break;

            yield Request(url, callback=self.parse_news)

        if is_scraped:
            self.logger.info('Media have no update')
            return

        if (len(articles) == 0):
            self.failed_count += 1
        else:
            self.failed_count = 0

        # Collect news on next page
        if response.css('.btn-loadmorenews1 > a'):
            next_page = response.css('.btn-loadmorenews1 > a::attr(href)').extract()[0]
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse)
        elif self.failed_count < 5:
            next_page = response.url.split('/')
            next_page[-1] = str(int(next_page[-1]) + 5)
            next_page_url = '/'.join(next_page)
            yield Request(next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)
        parsed_news = json.loads(str(response.body))
        parsed_news = parsed_news[0]

        # Initialize item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)

        loader.add_value('url', response.url)

        if not parsed_news['title']:
            # Will be dropped on the item pipeline
            return loader.load_item()
        loader.add_value('title', parsed_news['title'])

        if not parsed_news['author']:
            # Will be dropped on the item pipeline
            return loader.load_item()
        loader.add_value('author_name', parsed_news['author'])

        if not parsed_news['content']:
            # Will be dropped on the item pipeline
            return loader.load_item()
        parsed_news['content'] = re.search(r'<body>(.*)</body>', parsed_news['content'], re.S|re.I).group(1)
        parsed_news['content'] = re.sub(r'<img[^>]+\>', '', parsed_news['content'])
        loader.add_value('raw_content', parsed_news['content'])

        if not parsed_news['published']:
            # Will be dropped on the item pipeline
            return loader.load_item()

        # Parse date information
        try:
            # Example: 12 Oct 2016 - 05:25
            date_time_str = ' '.join([_(w) for w in parsed_news['published'].split(',')[1].strip()[:-4].split(' ')])
            self.logger.info('parse_date: parse_news: date_str: %s', date_time_str)
            published_at = wib_to_utc(
                            datetime.strptime(date_time_str,'%d %b %Y - %H:%M'))
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: %s' % e)

        # Move scraped news to pipeline
        return loader.load_item()
