# -*- coding: utf-8 -*-
from rojak_pantau.spiders.base import BaseSpider
from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader

from rojak_pantau.items import News
from rojak_pantau.i18n.i18n import i18n
from rojak_pantau.util.wib_to_utc import wib_to_utc

class KompasComSpider(BaseSpider):
    name = "kompas"
    start_urls = [
        'http://lipsus.kompas.com/topikpilihanlist/3754/1/Pilkada.DKI.2017'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
    }
    translator = i18n()

    def parse(self, response):
        is_no_update = False

        news_selector = response.css("ul.clearfix > li > div.tleft")
        if not news_selector:
            raise CloseSpider('news_selectors not found')
        for news in news_selector:
            url_selectors = news.css("div.tleft > h3 > a::attr(href)")
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            date_selectors = news.css("div.grey.small::text")
            if not date_selectors:
                raise CloseSpider('date_selectors not found')
            raw_date = date_selectors.extract()[0]

            # Parse date information
            try:
                published_at = self.convert_date(raw_date);
            except Exception as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break

            # For each url we create new scrapy request
            yield Request(url=url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        np_selectors = response.css("ul.paginasi.mt2 > li > a::attr(href)")
        if not np_selectors:
            raise CloseSpider('np_selectors not found')
        next_pages = np_selectors.extract()
        for next_url in next_pages:
            yield Request(next_url, callback=self.parse)

    def convert_date(self, idn_date):
        # Example Rabu, 12 Oktober 2016 | 10:23 WIB
        info_time = idn_date.split(',')[1].strip().split('|');
        info_date = info_time[0].strip().split(' ');
        info_hours = info_time[1].strip().split(' ')[0].strip();
        day = info_date[0];
        month = self.translator.translate('idn')[info_date[1]];
        year = info_date[2];
        formatted_date = day+' '+month+' '+year+', ' + info_hours;
        return  wib_to_utc(datetime.strptime(formatted_date, '%d %B %Y, %H:%M'));

    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title_selectors = response.css("div.kcm-read-top > h2::text")
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title)

        raw_content_selectors = response.css("div.kcm-read-text > p")
        if not raw_content_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        raw_content = raw_content_selectors.extract()[0]
        loader.add_value('raw_content', raw_content)

        date_selectors = response.css("div.kcm-date::text")
        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        date = date_selectors.extract()[0];
        try:
            published_at = self.convert_date(date)
        except Exception:
            # Will be dropped on the item pipeline
            return loader.load_item()
        loader.add_value('published_at', published_at)

        author_name_selectors = response.css("span.pb_10::text")
        if not author_name_selectors:
            author_name = ''
            loader.add_value('author_name', author_name)
        else:
            author_name = ', '.join(author_name_selectors.extract())
            loader.add_value('author_name', author_name)

        return loader.load_item()

