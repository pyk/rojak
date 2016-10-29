# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.loader import ItemLoader

from rojak_pantau.items import News
from rojak_pantau.i18n import _
from rojak_pantau.util.wib_to_utc import wib_to_utc
from rojak_pantau.spiders.base import BaseSpider

NEWS_HEADLINE = 'headline'
NEWS_GRID = 'grid'

class MetrotvnewsSpider(BaseSpider):
    name = "metrotvnews"
    allowed_domains = ["metrotvnews.com"]
    start_urls = (
        'http://www.metrotvnews.com/more/topic/8602/0',
    )

    def parse(self, response):
        self.logger.info('parse: {}'.format(response))
        is_no_update = False

        # Collect list of news from current page
        articles_grid = response.css('li:not(.last) > div.grid')
        articles = zip(articles_grid, [NEWS_GRID] * len(articles_grid))
        articles += zip(response.css('div.topic'), [NEWS_HEADLINE])

        if not articles:
            raise CloseSpider('article not found')

        for article in articles:
            # Close the spider if we don't find the list of urls
            url_selectors = None
            if article[1] == NEWS_GRID:
                url_selectors = article[0].css('h2 > a::attr(href)')
            elif article[1] == NEWS_HEADLINE:
                url_selectors = article[0].css('h1 > a::attr(href)')

            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            self.logger.info('Url: {}'.format(url))

            # Example: Minggu, 09 Oct 2016 15:14
            info_selectors = article[0].css('div.reg::text')
            if not info_selectors:
                raise CloseSpider('info_selectors not found')
            info = info_selectors.extract()[1]
            # Example: 09 Oct 2016 15:14
            info_time = info.split(',')[1].strip()

            # Parse date information
            try:
                published_at_wib = datetime.strptime(info_time, '%d %b %Y %H:%M')
            except ValueError as e:
                raise CloseSpider('cannot_parse_date: {}'.format(e))

            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break
            # For each url we create new scrapy request
            yield Request(url, callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        # Collect news on next page
        if response.css('div.bu.fr > a'):
            next_page = response.css('div.bu.fr > a[rel="next"]::attr(href)').extract()[0]
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: {}'.format(response))
        is_video = response.css('ul.breadcrumb > li > a::text').extract()[0] == 'VIDEO'

        # Init item loader
        # extract news title, published_at, author, content, url
        # Required: title, raw_content, published_at
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        # Will be dropped if video page
        if is_video:
            return loader.load_item()

        title_selectors = response.css('div.part.lead.pr > h1::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title)

        xpath_query = """
            //div[@class="part article"]/node()
                [not(
                    descendant-or-self::comment()|
                    descendant-or-self::style|
                    descendant-or-self::script|
                    descendant-or-self::div|
                    descendant-or-self::span|
                    descendant-or-self::img|
                    descendant-or-self::table|
                    descendant-or-self::iframe
                )]
        """
        raw_content_selectors = response.xpath(xpath_query)
        if not raw_content_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        raw_content = raw_content_selectors.extract()
        raw_content = ' '.join([w.strip() for w in raw_content])
        raw_content = raw_content.strip()
        loader.add_value('raw_content', raw_content)

        # Example: Bambang - 10 Oktober 2016 21:10 wib
        info_selectors = response.css('div.part.lead.pr > span::text')
        if not info_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        info = info_selectors.extract()[0]

        # Parse date information
        # Example: 10 Oktober 2016 21:10 wib
        date_str = info.split('-')[1].strip()
        if not date_str:
            # Will be dropped on the item pipeline
            return loader.load_item()

        # Example: 10 October 2016 21:10
        date_str = ' '.join([_(w) for w in date_str[:-4].split(' ')])
        try:
            published_at_wib = datetime.strptime(date_str, '%d %B %Y %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        author_name = info.split('-')[0].strip()
        if not author_name:
            loader.add_value('author_name', '')
        else:
            loader.add_value('author_name', author_name)

        # Move scraped news to pipeline
        return loader.load_item()
