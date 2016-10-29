# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

from rojak_pantau.items import News
from rojak_pantau.i18n import _
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

class JawaposSpider(BaseSpider):
    name = "jawapos"
    allowed_domains = ["jawapos.com"]
    start_urls = (
        'http://www.jawapos.com/indextag?tag=Pilkada+DKI',
    )

    def parse(self, response):
        self.logger.info('parse: %s' % response)
        has_no_update = False

        # Get list of news from the current page
        for article in response.css('.col-sm-16 > .row > .col-sm-16 > .row'):
            title = article.css('h4::text').extract_first()
            url = article.css('a::attr(href)').extract_first()            
            time = article.css('.indexTime::text').extract_first() # 16:51

            date = article.css('.indexDay::text').extract_first() # Sabtu, 15 Oktober 2016
            date = date.split(',')[-1].strip() # 15 Oktober 2016

            date_time = date + ' ' + time # 15 Oktober 2016 16:51
            date_time = date_time.split(' ')
            date_time = ' '.join([_(s) for s in date_time]) # Oktober => October

            # Parse date information
            try:
                published_at_wib = datetime.strptime(date_time, '%d %B %Y %H:%M')
            except ValueError as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                has_no_update = True
                break

            # For each url we create new scrapy request
            yield Request(url, callback=self.parse_news)

        if has_no_update:
            self.logger.info('Media have no update')
            return

        # Currently has no more pages

    def parse_multipage_content(self, response):
        loader = response.meta['loader']
        n = response.meta['n']

        raw_content_selectors = response.css('.newsContent > p') # The news
        raw_content = ' '.join(raw_content_selectors.extract())
        raw_content = raw_content.strip()

        # Get page number from the back of a URL
        # Example: http://www.jawapos.com/.../3
        page = response.url[response.url.rindex('/')+1:]
        loader.add_value('raw_content', {'page': page, 'content': raw_content})

        rc = loader.get_collected_values('raw_content')

        # If current page is the last, get the author name
        if int(page) == n:
            author_name_selectors = response.css('.newsContent > p > strong::text')
            author_name = author_name_selectors.extract()[-1].strip()
            loader.add_value('author_name', author_name)

        # when we get all the pages, concatenate the parts into raw_content
        if len(rc) == n:
            rc.sort(key=lambda x: x['page'])
            raw_content = ''.join(map(lambda x: x['content'], rc))
            loader.replace_value('raw_content', raw_content)
            return loader.load_item()

    def parse_indices(self, indices, loader):
        for index in indices:
            page_url = index.css('a::attr(href)').extract_first()

            yield Request(page_url, meta={'loader': loader, 'n': len(indices)},
                    callback=self.parse_multipage_content)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        # Required: title, raw_content, published_at
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title_selectors = response.css('h1.detailtitle::text')
        if not title_selectors:
            # If error, drop from the item pipeline
            return loader.load_item()
        title = title_selectors.extract_first().strip()
        loader.add_value('title', title)

        # Parse date information
        date_time = response.css('body > div > div.container > div.page-header > div::text').extract_first().strip()
        date_time = date_time.split(',')[-1].strip()
        date_time = ' '.join([_(w) for w in date_time.split(' ')]) # October => Oktober
        try:
            published_at_wib = datetime.strptime(date_time, '%d %B %Y %H:%M')
        except ValueError:
            # If error, drop from the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        # If multipage
        multipage_selectors = response.css('.newsPagingWrap > a')
        if multipage_selectors:
            return self.parse_indices(multipage_selectors, loader)

        # Else if not multipage

        author_name_selectors = response.css('.newsContent > p > strong::text')
        if not author_name_selectors:
            loader.add_value('author_name', '')
        else:
            author_name = author_name_selectors.extract()[-1].strip()
            loader.add_value('author_name', author_name)

        # Extract the news content
        raw_content_selectors = response.css('.newsContent > p')
        if not raw_content_selectors:
            # Drop from the item pipeline
            return loader.load_item()
            
        raw_content = ' '.join(raw_content_selectors.extract())
        raw_content = raw_content.strip()
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
