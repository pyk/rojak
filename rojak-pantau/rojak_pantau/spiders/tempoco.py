# -*- coding: utf-8 -*-
import json

from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.i18n import _
from rojak_pantau.spiders.base import BaseSpider

class TempocoSpider(BaseSpider):
    name="tempo.co"
    allowed_domains = ["tempo.co"]
    start_urls = (
        'http://www.tempo.co/topik/masalah/1432/pilkada-dki-jakarta',
    )
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    def parse(self, response):
        # Latest news
        url_selector = response.css('.block-display h1 a::attr(href)')
        if url_selector:
            yield Request(url_selector.extract()[0], callback=self.parse_news_metro)

        # News list
        url_list_selector = response.css('#sub-news ul.list-terkini li .box-text a::attr(href)')
        if url_list_selector:
            for url in url_list_selector.extract():
                yield Request(url, callback=self.parse_news_metro)

    # For pilkada.tempo.co
    # NOTE: I never encounter a page in pilkada.tempo.co that have multiple page
    # This function only able to handle a single pilkada.tempo.co page
    def parse_news_pilkada(self, loader, response):
        date_selector = response.css('.block-judul-artikel > .tanggal::text')
        try:
            date_time_str = date_selector.extract()[0].split(',')[1].strip()[:-4]
            date_time_str = ' '.join([_(x) for x in date_time_str.split(' ')])
            published_at_wib = datetime.strptime(date_time_str, '%d %B %Y | %H:%M')
        except Exception:
            return loader.load_item()
        published_at = wib_to_utc(published_at_wib)

        if (self.media['last_scraped_at'] >= published_at):
            is_no_update = True
            self.logger.info('Media have no update')
            raise CloseSpider('finished')
        loader.add_value('published_at', published_at)

        title_selector = response.css('.block-judul-artikel > .judul-artikel')
        loader.add_value('title', title_selector.extract()[0])

        raw_content_selector = response.css('.block-artikel .p-artikel')
        raw_content_selector = raw_content_selector.xpath('//p[not(iframe)]')
        raw_content = ''
        for rsl in raw_content_selector:
            raw_content = raw_content + rsl.extract().strip()
        loader.add_value('raw_content', raw_content)

        author_name = ''
        for author_name_selector in reversed(raw_content_selector):
            author_name_selector = author_name_selector.css('strong::text')
            for tmp in reversed(author_name_selector.extract()):
                tmp = tmp.strip()
                if tmp and all((x.isalpha() and x.isupper()) or x.isspace() or x == '.' or x == '|' for x in tmp):
                    author_name = tmp
                    break
            if author_name:
                break
        author_name = ','.join(author_name.split(' | '))
        loader.add_value('author_name', author_name)
        loader.add_value('url', response.url)

    def parse_next_page_metro(self, response, loader, raw_content):
        raw_content_selector = response.xpath('//div[@class="artikel"]//p[not(iframe)]')

        for rsl in raw_content_selector:
            raw_content = raw_content + rsl.extract().strip()

        next_page_selector = response.css('.pagination-nb').xpath('//a[text()="next"]/@href')
        if next_page_selector:
            return Request(next_page_selector.extract()[0], callback=lambda x, loader=loader, raw_content=raw_content: self.parse_next_page_metro(x, loader, raw_content))

        loader.add_value('raw_content', raw_content)

        author_name = ''
        for author_name_selector in reversed(raw_content_selector):
            author_name_selector = author_name_selector.css('strong::text')
            for tmp in reversed(author_name_selector.extract()):
                tmp = tmp.strip()
                if tmp and all((x.isalpha() and x.isupper()) or x.isspace() or x == '.' or x == '|' for x in tmp):
                    author_name = tmp
                    break
            if author_name:
                break
        author_name = ','.join(author_name.split(' | '))
        loader.add_value('author_name', author_name)
        return loader.load_item()

    # For *.tempo.co
    def parse_news_metro(self, response):
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        date_selector = response.css('.artikel > div.block-tanggal::text')
        if not date_selector:
            return self.parse_news_pilkada(loader, response)
        try:
            date_time_str = date_selector.extract()[0].split(',')[1].strip()[:-4]
            date_time_str = ' '.join([_(x) for x in date_time_str.split(' ')])
            published_at_wib = datetime.strptime(date_time_str, '%d %B %Y | %H:%M')
        except Exception:
            return loader.load_item()
        published_at = wib_to_utc(published_at_wib)
        if (self.media['last_scraped_at'] >= published_at):
            is_no_update = True
            self.logger.info('Media have no update')
            raise CloseSpider('finished')
        loader.add_value('published_at', published_at)

        title_selector = response.css('.artikel > h1::text')
        if not title_selector:
            return loader.load_item()
        loader.add_value('title', title_selector.extract()[0])

        # Select all p which don't have iframe inside it
        raw_content_selector = response.xpath('//div[@class="artikel"]//p[not(iframe)]')
        if not raw_content_selector:
            return loader.load_item()
        raw_content = ''
        for rsl in raw_content_selector:
            raw_content = raw_content + rsl.extract().strip()

        # Go to next page while there is next page button
        next_page_selector = response.css('.pagination-nb').xpath('//a[text()="next"]/@href')
        if next_page_selector:
            return Request(next_page_selector.extract()[0], callback=lambda x, loader=loader, raw_content=raw_content: self.parse_next_page_metro(x, loader, raw_content))

        loader.add_value('raw_content', raw_content)

        # The author usually put inside <strong> tag, however, some news is not using <strong> tag.
        # NOTE: this block of code may need revision in the future
        author_name = ''
        for author_name_selector in reversed(raw_content_selector):
            author_name_selector = author_name_selector.css('strong::text')
            for tmp in reversed(author_name_selector.extract()):
                tmp = tmp.strip()
                if tmp and all((x.isalpha() and x.isupper()) or x.isspace() or x == '.' or x == '|' for x in tmp):
                    author_name = tmp
                    break
            if author_name:
                break
        author_name = ','.join(author_name.split(' | '))
        loader.add_value('author_name', author_name)
        return loader.load_item()
