# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.util.month import sanitize
from rojak_pantau.spiders.base import BaseSpider

import re
import json
from datetime import datetime, timedelta

class ArahSpider(BaseSpider):
    name = "arah"
    allowed_domains = ["arah.com"]
    start_urls = [
            'http://pilkada.arah.com/api/article/8/' + str(datetime.now())[:19]
    ]

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        is_no_update = False
        published_at_wib = ''

        try:
            # Get list of news from the current page
            articles = json.loads(response.text)

            for article in articles['contents']:
                url = article['friendlyURL']
                date = article['publishTime']
                published_at_wib = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                published_at = wib_to_utc(published_at_wib)

                if self.media['last_scraped_at'] >= published_at:
                    is_no_updated = True
                    break

                yield Request('http://pilkada.arah.com' + url, callback=self.parse_news)
        except:
            raise CloseSpider('article not found')

        if is_no_update:
            self.logger.info('Media have no update')
            return

        # Get more
        try:
            next_date = published_at_wib - timedelta(seconds=1)

            if self.media['last_scraped_at'] < wib_to_utc(next_date):
                yield Request('http://pilkada.arah.com/api/article/8/' + str(next_date)[:19],
                        callback=self.parse)
        except:
            pass

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        # Required: title, raw_content, published_at
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title_selectors = response.css('article > h1.title::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title.strip())

        # Parse date information
        # Example: 15 November, 2016
        date_selectors = response.css('article > h5.date::text')

        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()

        try:
            tmp = date_selectors.extract()[0].strip().split('|')
            date = (tmp[0].split(', ')[1].strip() + "|" + tmp[1].strip()).split()
            date[1] = sanitize(date[1])
            published_at_wib = datetime.strptime(' '.join(date), '%d %b %Y|%H:%M WIB')

            author = ''
            try:
                author = tmp[2].split(':')[1].strip()
            except:
                pass
            loader.add_value('author_name', author)
        except:
            # Will be dropped on the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        # Extract the content using XPath instead of CSS selector
        # We get the XPath from chrome developer tools (copy XPath)
        # or equivalent tools from other browser
        xpath_query = """
            //article[@class="artikel-inside"]/node()
                 [not(
                     descendant-or-self::comment()|
                     descendant-or-self::style|
                     descendant-or-self::script|
                     descendant-or-self::div|
                     descendant-or-self::span|
                     descendant-or-self::img|
                     descendant-or-self::table|
                     descendant-or-self::iframe|
                     descendant-or-self::h1|
                     descendant-or-self::h5|
                     descendant-or-self::figure
                 )]
         """
        raw_content_selectors = response.xpath(xpath_query)
        if not raw_content_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        raw_content = raw_content_selectors.extract()
        raw_content = ' '.join([w.encode('ascii', 'ignore').strip() for w in raw_content])
        raw_content = re.sub(r'<p><strong>Baca Juga:.*?</p>', '', raw_content.strip())
        raw_content = re.sub(r'<p><strong>Berita Terkait:.*</p>', '', raw_content.strip())
        # get rid of links
        raw_content = re.sub(r'<a.*?>(.*?)</a>', r'\1', raw_content.strip())
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
