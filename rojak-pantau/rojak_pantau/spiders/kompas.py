# -*- coding: utf-8 -*-
from rojak_pantau.spiders.base import BaseSpider
from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader

import json

from rojak_pantau.items import News
from rojak_pantau.i18n.i18n import i18n
from rojak_pantau.util.wib_to_utc import wib_to_utc

class KompasSpider(BaseSpider):
    name = "kompas"
    start_urls = [
        'http://lipsus.kompas.com/topikpilihanlist/3754/1/Pilkada.DKI.2017'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
    }
    translator = i18n()
    first_time = True

    def parse(self, response):
        is_no_update = False

        news_selector = response.css("ul.clearfix > li > div.tleft")
        if not news_selector:
            raise CloseSpider('news_selectors not found')
        for news in news_selector:
            url_selectors = news.css("div.tleft > h3 > a::attr(href)")
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            # http://megapolitan.kompas.com/read/xml/2016/10/18/17244781/ini.alat.peraga.kampanye.yang.boleh.dibuat.cagub-cawagub.dki
            # http://api.kompas.com/external/?type=readdua&kanal=home&command=.xml.2016.10.15.07300081&format=json&APPSF0UNDRYBYPASS=%20HTTP/1.1
            url = url_selectors.extract()[0]
            url = 'http://api.kompas.com/external/?type=readdua&kanal=home&command=.xml.' + '.'.join(url.split('/')[-5:-1]) + '&format=json&APPSF0UNDRYBYPASS=%20HTTP/1.1'

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

        # For kompas case, we don't rely on the pagination
        # Their pagination is max 17 pages, the truth is they have 25 pages
        if self.first_time:
            template_url = 'http://lipsus.kompas.com/topikpilihanlist/3754/{}/Pilkada.DKI.2017'
            for i in xrange(25):
                page = i + 1
                next_url = template_url.format(page)
                yield Request(next_url, callback=self.parse)
            self.first_time = False

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
        json_response = json.loads(response.body)

        try:
            url = json_response['NewsML']['NewsItem']['NewsComponent']['NewsComponent']['NewsComponent']['NewsLines']['MoreLink']
        except KeyError:
            return loader.load_item()
        loader.add_value('url', url)

        try:
            title = json_response['NewsML']['NewsItem']['NewsComponent']['NewsComponent']['NewsComponent']['NewsLines']['HeadLine']
        except KeyError:
            return loader.load_item()
        if not title:
            return loader.load_item()
        loader.add_value('title', title)

        try: 
            raw_content = json_response['NewsML']['NewsItem']['NewsComponent']['NewsComponent']['NewsComponent']['ContentItem']['DataContent']['nitf']['body']['body.content']['p']
        except KeyError:
            return loader.load_item()
        if not raw_content:
            return loader.load_item()
        loader.add_value('raw_content', raw_content)

        try:
            author_name = json_response['NewsML']['NewsItem']['NewsComponent']['NewsComponent']['Author']
        except KeyError:
            return loader.load_item()
        if not author_name:
            loader.add_value('author_name', '')
        else:
            loader.add_value('author_name', author_name)

        try:
            date_time_str = json_response['NewsML']['NewsItem']['NewsManagement']['FirstCreated']
        except KeyError:
            return loader.load_item()
        if not date_time_str:
            return loader.load_item()

        date_time_str = date_time_str.split('T')
        date_time_str[1] = '0' * (6 - len(date_time_str[1])) + date_time_str[1]
        try:
            published_at_wib = datetime.strptime(' '.join(date_time_str), '%Y%m%d %H%M%S');
        except Exception:
            return loader.load_item()
        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        return loader.load_item()
