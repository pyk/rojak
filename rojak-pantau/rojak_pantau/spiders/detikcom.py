# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from rojak_pantau.items import News
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

class DetikcomSpider(BaseSpider):
    name = "detikcom"
    allowed_domains = ["detik.com"]
    start_urls = (
        'http://m.detik.com/news/indeksfokus/67/jakarta-memilih/1',
    )

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        is_scraped = False

        # Get list of news from the current page
        for article in response.css('article'):
            url = article.css('a::attr(href)').extract()[0]
            # Example 'detikNews | Sabtu 08 Oct 2016, 14:54 WIB'
            info = article.css('a > .text > span.info::text').extract()[0]

            # Parse date information
            try:
                # Example 'Sabtu 08 Oct 2016, 14:54 WIB'
                info_time = info.split('|')[1].strip()
                # Example '08 Oct 2016, 14:54'
                info_time = ' '.join(info_time.split(' ')[1:5])
                self.logger.info('info_time: %s', info_time)
                published_at_wib = datetime.strptime(info_time,
                    '%d %b %Y, %H:%M')
                published_at = wib_to_utc(published_at_wib)
            except Exception as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            if self.media['last_scraped_at'] >= published_at:
                is_scraped = True
                break
            # For each url we create new scrapy request
            yield scrapy.Request(url, callback=self.parse_news)

        if is_scraped:
            self.logger.info('Media have no update')
            return

        if response.css('a.btn_more'):
            next_page = response.css('a.btn_more::attr(href)')[0].extract()
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)
        elif response.css('div.pag-nextprev > a'):
            next_page = response.css('div.pag-nextprev > a::attr(href)')[1].extract()
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)
        title = response.css('div.detail_area > h1.jdl::text').extract()[0]
        loader.add_value('title', title)
        author_name = response.css('div.author > strong::text').extract()[0]
        loader.add_value('author_name', author_name)
        raw_content = response.css('article > div.text_detail').extract()[0]
        loader.add_value('raw_content', raw_content)

        # Parse date information
        try:
            # Example: Kamis 15 Sep 2016, 18:33 WIB
            date_str = response.css('div.detail_area > div.date::text').extract()[0]
            # Example: '15 Sep 2016, 18:33'
            date_str = ' '.join(date_str.split(' ')[1:5])
            self.logger.info('parse_date: parse_news: date_str: %s', date_str)
            published_at = datetime.strptime(date_str,
                '%d %b %Y, %H:%M')
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: %s' % e)

        # Move scraped news to pipeline
        return loader.load_item()

