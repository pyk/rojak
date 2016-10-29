# -*- coding: utf-8 -*-
from scrapy import signals, Request
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy.loader import ItemLoader

from rojak_pantau.spiders.base import BaseSpider

from datetime import datetime

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.i18n import _

class SindonewsSpider(BaseSpider):
    name="sindonews"
    allowed_domains=["sindonews.com"]
    start_urls=(
        'http://metro.sindonews.com/topic/7282/pilgub-dki/',
    )

    def parse(self, response):
        self.logger.info('parse: {}'.format(response))
        is_no_update = False

        for article in response.css('li > div.breaking-title'):
            # http://metro.sindonews.com/read/1146316/171/penyidik-bareskrim-mulai-dalami-video-dugaan-penistaan-agama-1476179831
            url_selectors = article.css('a::attr(href)')

            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example 'Kamis, 13 Oktober 2016 - 11:18 WIB'
            date_time_str_selectors = article.css('p::text')

            if not date_time_str_selectors:
                raise CloseSpider('date_time_str_selectors not found')

            date_time_str = date_time_str_selectors.extract()[0]

            # Parse date information
            # Example '13 Oktober 2016 - 11:18'
            date_time_str = date_time_str.split(',')[1].strip()[:-4]
            date_time_str = ' '.join([_(w) for w in date_time_str.split(' ')])
            try:
                published_at_wib = datetime.strptime(date_time_str, '%d %B %Y - %H:%M')
            except Exception as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break

            # For each url we create new scrapy request
            yield Request(url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        for next_button in response.css('.mpaging > ul > li'):
            if len(next_button.css('a:not(.active) > .fa-angle-right')) > 0:
              next_page = next_button.css('a::attr(href)').extract()[0]
              next_page_url = response.urljoin(next_page)
              yield Request(next_page_url, callback=self.parse)
              break

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title_selectors = response.css('h1[itemprop="headline"]::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title)


        author_name_selectors = response.css('a[rel="author"] > span::text')
        if not author_name_selectors:
            loader.add_value('author_name', '')
        else:
            author_name = author_name_selectors.extract()[0]
            loader.add_value('author_name', author_name)

        raw_content_selectors = response.css('.content')
        if not raw_content_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        raw_content = raw_content_selectors.extract()
        raw_content = ' '.join([w.strip() for w in raw_content])
        raw_content = raw_content.strip()
        loader.add_value('raw_content', raw_content)

        date_time_str_selectors = response.css('article > div.time::text')
        if not date_time_str_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()

        # Parse date information
        # Example: Selasa,  6 Oktober 2015 - 05:23 WIB
        date_time_str = date_time_str_selectors.extract()[0]
        date_time_str = date_time_str.split(',')[1].strip()[:-4]
        date_time_str = ' '.join([_(w) for w in date_time_str.split(' ')])
        try:
            published_at_wib = datetime.strptime(date_time_str, '%d %B %Y - %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()
        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        # Move scraped news to pipeline
        return loader.load_item()
