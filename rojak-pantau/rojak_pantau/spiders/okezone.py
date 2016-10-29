# -*- coding: utf-8 -*-
import re
import json
from datetime import datetime

from scrapy import signals, Request
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.i18n import _
from rojak_pantau.spiders.base import BaseSpider

class OkezoneSpider(BaseSpider):
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

    def parse(self, response):
        self.logger.info('parse: {}'.format(response))
        is_no_update = False

        # Collect list of news from current page
        article_selectors = response.css('li.col-md-12')
        if not article_selectors:
            raise CloseSpider('article_selectors not found')
        for article in article_selectors:
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
            # Example: 12 October 2016 06:44
            # Remove WIB and convert the date to International based
            date_time_str = date_time_str.split(',')[1].strip();
            date_time_str = ' '.join([_(w) for w in date_time_str[:-4].split(' ')])
            try:
                published_at_wib = datetime.strptime(date_time_str,
                        '%d %B %Y %H:%M')
            except Exception as e:
                raise CloseSpider('cannot_parse_date: {}'.format(e))
            published_at = wib_to_utc(published_at_wib)

            if (self.media['last_scraped_at'] >= published_at):
                is_no_update = True
                break;

            yield Request(url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        if (len(article_selectors) == 0):
            self.failed_count += 1
        else:
            self.failed_count = 0

        # Collect news on next page
        if response.css('.btn-loadmorenews1 > a'):
            np_selectors = response.css('.btn-loadmorenews1 > a::attr(href)')
            next_page = np_selectors.extract()[0]
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
        parsed_news = json.loads(str(response.body))[0]

        # Initialize item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', parsed_news['url'])

        if not parsed_news['title']:
            # Will be dropped on the item pipeline
            return loader.load_item()
        loader.add_value('title', parsed_news['title'])

        # Convert HTML text to a scrapy response
        html_response = HtmlResponse(url=parsed_news['url'],
                body=parsed_news['content'].encode('utf-8', 'ignore'))
        xpath_query = '''
            //body/node()
                [not(descendant-or-self::comment()|
                    descendant-or-self::style|
                    descendant-or-self::script|
                    descendant-or-self::div|
                    descendant-or-self::span|
                    descendant-or-self::image|
                    descendant-or-self::img|
                    descendant-or-self::iframe
                )]
        '''
        raw_content_selectors = html_response.xpath(xpath_query)
        if not raw_content_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        raw_content = raw_content_selectors.extract()
        raw_content = ' '.join([w.strip() for w in raw_content])
        raw_content = raw_content.strip()
        loader.add_value('raw_content', raw_content)

        if not parsed_news['published']:
            # Will be dropped on the item pipeline
            return loader.load_item()

        # Parse date information
        # Example: 12 Oct 2016 - 05:25
        date_time_str = ' '.join([_(w) for w in parsed_news['published'].split(',')[1].strip()[:-4].split(' ')])
        try:
            published_at_wib = datetime.strptime(date_time_str,
                    '%d %b %Y - %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()
        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        if not parsed_news['author']:
            loader.add_value('author_name', '')
        else:
            loader.add_value('author_name', parsed_news['author'])

        # Move scraped news to pipeline
        return loader.load_item()

