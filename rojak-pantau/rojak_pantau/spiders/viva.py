# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader

from rojak_pantau.items import News
from rojak_pantau.i18n import _
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

class VivaSpider(BaseSpider):
    name = "viva"
    allowed_domains = ["viva.co.id"]
    start_urls = [
        'http://www.viva.co.id/tag/Pilkada-DKI-Jakarta-2017/1',
        'http://www.viva.co.id/tag/Pilkada-DKI-2017/1',
        'http://www.viva.co.id/tag/pilkada-dki/1'
    ]

    def parse(self, response):
        self.logger.info('parse: {}'.format(response))
        is_scraped = False

        # Collect list of news from current page
        for article in response.css('ul.indexlist > li'):
            url = article.css('a::attr(href)').extract()[0]
            # Example: 7 Oktober 2016 19:37
            info = article.css('div.upperdeck::text').extract()[1]
            info = info.split(',')[1].replace('\t','').strip()

            # Parse date information
            try:
                # Example: 7 October 2016 19:37
                info_time = info.split(' ')
                info_time = ' '.join([_(s) for s in info_time])
                self.logger.info('info_time: {}'.format(info_time))
                published_at_wib = datetime.strptime(info_time, '%d %B %Y %H:%M')
                published_at = wib_to_utc(published_at_wib)
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

        # Collect news on next page
        for tag in response.css('div.pagination > a'):
            more = tag.css('a::text').extract()[0]
            if more == 'NEXT':
                next_page = tag.css('a::attr(href)').extract()[0]
                next_page_url = response.urljoin(next_page)
                yield Request(next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: {}'.format(response))

        # Init item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title = response.css('h1.title-big-detail::text').extract()[0].strip()
        info = response.css('span.meta-author span::text').extract()
        author_name = info[0].strip()
        # Example: Sabtu, 1 Oktober 2016, 15:47 WIB
        date_str = info[-1].strip()
        # Extract raw html, not the text
        raw_content = response.css('div.detail-content').extract()[0]

        # Parse date information
        try:
            # Example: 1 October 2016 15:47
            date_str = date_str.replace(',', '').split(' ')[1:-1]
            date_str = ' '.join([_(s) for s in date_str])
            self.logger.info('parse_date: parse_news: date_str: {}'.format(date_str))

            published_at_wib = datetime.strptime(date_str, '%d %B %Y %H:%M')
            published_at = wib_to_utc(published_at_wib)
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: {}'.format(e))

        loader.add_value('title', title)
        loader.add_value('author_name', author_name)
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
