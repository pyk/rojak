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
        is_no_update = False

        # Collect list of news from current page
        article_selectors = response.css('ul.indexlist > li')
        if not article_selectors:
            raise CloseSpider('article_selectors not found')
        for article in article_selectors:
            url_selectors = article.css('a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example: 7 Oktober 2016 19:37
            info_selectors = article.css('div.upperdeck::text')
            if not info_selectors:
                raise CloseSpider('info_selectors not found')
            info = info_selectors.extract()[1]
            info = info.split(',')[1].replace('\t','').strip()
            # Example: 7 October 2016 19:37
            info_time = info.split(' ')
            info_time = ' '.join([_(s) for s in info_time])

            # Parse date information
            try:
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

        # Collect news on next page
        tag_selectors = response.css('div.pagination > a')
        if not tag_selectors:
            raise CloseSpider('tag_selectors not found')
        for tag in tag_selectors:
            more_selectors = tag.css('a::text')
            if not more_selectors:
                raise CloseSpider('more_selectors not found')
            more = more_selectors.extract()[0]
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

        title_selectors = response.css('h1.title-big-detail::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0].strip()
        loader.add_value('title', title)

        # Extract raw html, not the text
        # We filter-out the noise: HTML comments, scripts, css styles etc
        xpath_query ='''
            //div[@class="detail-content"]/node()
                [not(
                    descendant-or-self::comment()|
                    descendant-or-self::style|
                    descendant-or-self::script|
                    descendant-or-self::div|
                    descendant-or-self::span|
                    descendant-or-self::img|
                    descendant-or-self::table|
                    descendant-or-self::iframe|
                    descendant-or-self::a[@class="share-btn-right shared"]
                )]
        '''
        raw_content_selectors = response.xpath(xpath_query)
        if not raw_content_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        raw_content = raw_content_selectors.extract()
        raw_content = ' '.join([w.strip() for w in raw_content])
        loader.add_value('raw_content', raw_content)

        date_selectors = response.css('span.meta-author > span:nth-child(3)::text')
        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        # Example: Sabtu, 1 Oktober 2016, 15:47 WIB
        date_str = date_selectors.extract()[0].strip()
        # Example: 1 October 2016 15:47
        date_str = date_str.replace(',', '').split(' ')[1:-1]
        date_str = ' '.join([_(s) for s in date_str])
        # Parse date information
        try:
            published_at_wib = datetime.strptime(date_str, '%d %B %Y %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()
        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        author_selectors = response.css('span.meta-author > span > b::text')
        if not author_selectors:
            author_name = ''
            loader.add_value('author_name', author_name)
        else:
            author_name = author_selectors.extract()[0]
            loader.add_value('author_name', author_name)

        # Move scraped news to pipeline
        return loader.load_item()

