# -*- coding: utf-8 -*-
import scrapy
import MySQLdb as mysql
import os
from datetime import datetime
from scrapy.exceptions import CloseSpider

ROJAK_DB_HOST = os.getenv('ROJAK_DB_HOST', 'localhost')
ROJAK_DB_PORT = int(os.getenv('ROJAK_DB_PORT', 3306))
ROJAK_DB_USER = os.getenv('ROJAK_DB_USER', 'root')
ROJAK_DB_PASS = os.getenv('ROJAK_DB_PASS', 'rojak')
ROJAK_DB_NAME = os.getenv('ROJAK_DB_NAME', 'rojak_database')

sql_get_media = '''
SELECT id,last_scraped_at FROM media WHERE name=%s;
'''

sql_insert_news = '''
INSERT INTO `news`(`media_id`, `title`, `raw_content`,
    `url`, `author_name`, `published_at`)
VALUES (%s, %s, %s, %s, %s, %s);
'''

# TODO: understanding di scheduler works not only once
# TODO: save state last_scraped_at
class DetikcomSpider(scrapy.Spider):
    name = "detikcom"
    allowed_domains = ["detik.com"]
    start_urls = (
        'http://m.detik.com/news/indeksfokus/67/jakarta-memilih/1',
    )

    def __init__(self):
        # Get media information from the database
        # Open database connection
        self.db = mysql.connect(host=ROJAK_DB_HOST, port=ROJAK_DB_PORT,
            user=ROJAK_DB_USER, passwd=ROJAK_DB_PASS, db=ROJAK_DB_NAME)
        self.cursor = self.db.cursor()

        # Using UTF-8 Encoding
        self.db.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

        self.media = {}
        try:
            self.logger.info('Fetching media information')
            self.cursor.execute(sql_get_media, [self.name])
            row = self.cursor.fetchone()
            self.media['id'] = row[0]
            self.media['last_scraped_at'] = row[1]
        except mysql.Error as err:
            self.logger.error('Unable to fetch media data: %s', err)
            raise scrapy.exceptions.NotConfigured('Unable to fetch media data')

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
                raise CloseSpider('parse: Cannot parse date: %s' % e)

            if media['last_scraped_at'] >= published_at:
                is_scraped = True
                break
            # For each url we create new scrapy request
            yield scrapy.Request(url, callback=self.parse_news)

        if is_scraped:
            return

        if response.css('a.btn_more'):
            next_page = response.css('a.btn_more::attr(href)')[0].extract()
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
        elif response.css('div.pag-nextprev > a'):
            next_page = response.css('div.pag-nextprev > a::attr(href)')[1].extract()
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    # Callback for parsing a news
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # extract news title, published_at, author, content, url
        url = response.url
        title = response.css('div.detail_area > h1.jdl::text').extract()[0]
        author_name = response.css('div.author > strong::text').extract()[0]
        raw_content = response.css('article > div.text_detail::text').extract()
        raw_content = ' '.join(raw_content)

        # Parse date information
        try:
            # Example: Kamis 15 Sep 2016, 18:33 WIB
            date_str = response.css('div.detail_area > div.date::text').extract()[0]
            # Example: '15 Sep 2016, 18:33'
            date_str = ' '.join(date_str.split(' ')[1:5])
            self.logger.info('parse_news: date_str: %s', date_str)
            published_at = datetime.strptime(date_str,
                '%d %b %Y, %H:%M')
        except Exception as e:
            raise CloseSpider('parse_news: Cannot parse date: %s' % e)

        # Insert to the database
        try:
            self.cursor.execute(sql_insert_news, [self.media['id'], title,
                raw_content, url, author_name, published_at])
            self.db.commit()
        except mysql.Error as err:
            self.db.rollback()
            raise CloseSpider('parse_news: Cannot save news: %s' % err)



