# -*- coding: utf-8 -*-
import json
import re
from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup

from rojak_pantau.items import News
from rojak_pantau.i18n import _
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

NEWS_LIMIT = 600
PARAMS = 'taglistdetail.php?catName=pilgub-dki-2017&p=1&limit={}'.format(NEWS_LIMIT)

class BeritasatuSpider(BaseSpider):
    name = "beritasatu"
    allowed_domains = ["beritasatu.com"]
    start_urls = [
        # Consume API directly, this returns JSON response
        'http://m.beritasatu.com/static/json/mobile/{}'.format(PARAMS)
    ]

    def parse(self, response):
        self.logger.info('parse: {}'.format(response))
        is_no_update = False

        # beritasatu response is HTML snippet wrapped in a JSON response
        json_response = json.loads(response.body_as_unicode())
        if not 'content' in json_response:
            raise CloseSpider('json_response invalid')
        data = json_response['content']
        response = HtmlResponse(url=response.url, body=data.encode('utf-8',
            'ignore'))

        # Note: no next page button on beritasatu, all is loaded here
        # adjust how many links to extract from NEWS_LIMIT const
        article_selectors = response.css('div.headfi')
        if not article_selectors:
            raise CloseSpider('article_selectors not found')
        for article in article_selectors:
            url_selectors = article.css('h4 > a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url_raw = url_selectors.extract()[0]
            url = 'http://www.beritasatu.com{}'.format(url_raw)

            # Example: Kamis, 06 Oktober 2016 | 10:11 -
            info_selectors = article.css('div.ptime > span.datep::text')
            if not info_selectors:
                raise CloseSpider('info_selectors not found')
            info = info_selectors.extract()[0]
            info_time = re.split('[\s,|-]', info)
            info_time = ' '.join([_(s) for s in info_time[1:] if s])

            # Parse date information
            try:
                # Example: 06 October 2016 10:11
                published_at_wib = datetime.strptime(info_time, '%d %B %Y %H:%M')
            except ValueError as err:
                raise CloseSpider('cannot_parse_date: {}'.format(err))

            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break
            # For each url we create new scrapy Request
            yield Request(url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

    def parse_news(self, response):
        self.logger.info('parse_news: {}'.format(response))

        # Init item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        xpath_title = '//h4[@class="content-detail-title"]'
        title_selectors = response.xpath(xpath_title)
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        # Example: 
        # [u'<h4 class="content-detail-title" align="center">
        # Median: <i>Swing Voters</i> di DKI Diprediksi 19,4 Persen</h4>']
        title_html_str = ' '.join(title_selectors.extract())
        # Clean the html tag
        # Example: u'Median: Swing Voters di DKI Diprediksi 19,4 Persen'
        title = BeautifulSoup(title_html_str, 'lxml').text
        loader.add_value('title', title.strip())

        # Extract raw html, not the text
        raw_content_selectors = response.css('div.content-body')
        if not raw_content_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        raw_content = raw_content_selectors.extract()
        raw_content = ' '.join([w.strip() for w in raw_content])
        raw_content = raw_content.strip()
        raw_content = raw_content.replace('\n', ' ')
        loader.add_value('raw_content', raw_content)

        # Example: Selasa, 11 Oktober 2016 | 10:48
        date_selectors = response.css('div.date::text')
        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        date_str = date_selectors.extract()[0]
        # Example: 11 October 2016 10:48
        date_str = re.split('[\s,|-]', date_str)
        date_str = ' '.join([_(s) for s in date_str[1:] if s])

        # Parse date information
        try:
            published_at_wib = datetime.strptime(date_str, '%d %B %Y %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()
        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        author_selectors = response.css('div.content-detail > p::text')
        if not author_selectors:
            loader.add_value('author_name', '')
        else:
            author_name = author_selectors.extract()[0]
            author_name = author_name.split('/')[0]
            loader.add_value('author_name', author_name)

        # Move scraped news to pipeline
        return loader.load_item()

