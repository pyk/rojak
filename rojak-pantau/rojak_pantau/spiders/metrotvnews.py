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


class MetrotvnewsSpider(Spider):
    name = "metrotvnews"
    allowed_domains = ["metrotvnews.com"]
    start_urls = (
        'http://www.metrotvnews.com/more/topic/8602/0',
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
        spider = super(MetrotvnewsSpider, cls).from_crawler(crawler,
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
        for i, article in enumerate(
                response.css('div.topic') + response.css('li:not(.last) > div.grid')):
            if i == 0:
                url = article.css('h1 > a::attr(href)').extract()[0]
            else:
                url = article.css('h2 > a::attr(href)').extract()[0]

            # Example: Minggu, 09 Oct 2016 15:14
            info = article.css('div.reg::text').extract()[1].strip()

            # Parse date information
            try:
                # Example: 09 Oct 2016 15:14
                info_time = info.split(',')[1].strip()
                self.logger.info('info_time: {}'.format(info_time))
                published_at = wib_to_utc(
                    datetime.strptime(info_time, '%d %b %Y %H:%M'))
            except Exception as e:
                raise CloseSpider('cannot_parse_date: {}'.format(e))

            if self.media['last_scraped_at'] >= published_at:
                is_scraped = True
                break
            # For each url we create new scrapy request
            yield Request(url, callback=self.parse_news)

        if is_scraped:
            self.logger.info('Media have no update')
            return

        # Collect news on next page
        if response.css('div.bu.fr > a'):
            next_page = response.css('div.bu.fr > a[rel="next"]::attr(href)').extract()[0]
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: {}'.format(response))
        is_video = response.css('ul.breadcrumb > li > a::text').extract()[0] == 'VIDEO'

        # Init item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        if is_video:
            title = response.css('div.part.detail > h1::text').extract()[0]
            author_name = None
            # Example: 10 Oktober 2016 21:10 wib
            date_str = response.css('span.r.mright::text').extract()[0]

        else:
            title = response.css('div.part.lead.pr > h1::text').extract()[0]
            info = response.css('div.part.lead.pr > span::text').extract()[0]
            author_name = info.split('-')[0].strip()
            # Example: 10 Oktober 2016 21:10 wib
            date_str = info.split('-')[1].strip()

        # Extract raw html, not the text
        raw_content = response.css('div.part.article').extract()
        raw_content = ' '.join(raw_content)
        # Parse date information
        try:
            # Example: 10 Oktober 2016 21:10
            date_str = ' '.join([_(w) for w in date_str[:-4].split(' ')])
            self.logger.info('parse_date: parse_news: date_str: {}'.format(date_str))
            published_at = wib_to_utc(
                datetime.strptime(date_str, '%d %B %Y %H:%M'))
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: {}'.format(e))

        loader.add_value('title', title)
        loader.add_value('author_name', author_name)
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
