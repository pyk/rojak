# -*- coding: utf-8 -*-
from rojak_pantau.spiders.base import BaseSpider
from datetime import datetime
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader

from rojak_pantau.items import News
from rojak_pantau.i18n import _
from rojak_pantau.util.wib_to_utc import wib_to_utc

class KompasComSpider(BaseSpider):
    name = "kompas"
    start_urls = [
        'http://lipsus.kompas.com/topikpilihanlist/3754/1/Pilkada.DKI.2017'
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'
    }

    def parse(self, response):
        is_scraped = False

        for news in response.css("ul.clearfix > li > div.tleft"):
            url = news.css("div.tleft > h3 > a::attr(href)").extract()[0]
            raw_date = news.css("div.grey.small::text").extract()[0]

            # Parse date information
            try:
                published_at = self.convert_date(raw_date);
            except Exception as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            if self.media['last_scraped_at'] >= published_at:
                is_scraped = True
                break
            #For each url we create new scrapy request
            yield scrapy.Request(url=url, callback=self.parse_news)

        if is_scraped:
            self.logger.info('Media have no update')
            return
    
        next_pages = response.css("ul.paginasi.mt2 > li > a::attr(href)").extract()
        for next_url in next_pages:
            yield scrapy.Request(next_url, callback=self.parse)

    def convert_date(self, idn_date):
        # Example Rabu, 12 Oktober 2016 | 10:23 WIB
        info_time = idn_date.split(',')[1].strip().split('|');
        info_date = info_time[0].strip().split(' ');
        info_hours = info_time[1].strip().split(' ')[0].strip();
        day = info_date[0];
        month = _(info_date[1]);
        year = info_date[2];
        formatted_date = day+' '+month+' '+year+', ' + info_hours;
        return  wib_to_utc(datetime.strptime(formatted_date, '%d %B %Y, %H:%M'));

    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)
        
        title = ' '.join(response.css("div.kcm-read-top > h2::text").extract())
        author_name = ', '.join(response.css("span.pb_10::text").extract())
        raw_content = response.css("div.kcm-read-text > p").extract()
        raw_content = ' '.join(raw_content)
        date = response.css("div.kcm-date::text").extract()[0];

        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)
        loader.add_value('title', title)
        loader.add_value('author_name', author_name)
        loader.add_value('raw_content', raw_content)
        loader.add_value('url', response.url)
        try:
            loader.add_value('published_at',self.convert_date(date))
        except Exception as e:
            raise CloseSpider('cannot_parse_date: %s' % e)
        
        return loader.load_item()
