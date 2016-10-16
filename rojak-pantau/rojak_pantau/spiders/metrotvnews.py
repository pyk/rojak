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
                url_selectors = article.css('h2 > a::attr(href)')
            elif article[1] == NEWS_HEADLINE:
                url_selectors = article.css('h1 > a::attr(href)')

            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example: Minggu, 09 Oct 2016 15:14
            info_selectors = article.css('div.reg::text')
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
                is_scraped = True
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

        # Skip if video page, since no author here
        if is_video:
            return

        # Init item loader
        # extract news title, published_at, author, content, url
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)

        title = response.css('div.part.lead.pr > h1::text').extract()[0]
        info = response.css('div.part.lead.pr > span::text').extract()[0]
        author_name = info.split('-')[0].strip()
        # Example: 10 Oktober 2016 21:10 wib
        date_str = info.split('-')[1].strip()

        # Extract raw html, not the text
        raw_content = response.css('div.part.article').extract()
        raw_content = ' '.join(raw_content)
        # Parse date information
        try:
            # Example: 10 October 2016 21:10
            date_str = ' '.join([_(w) for w in date_str[:-4].split(' ')])
            self.logger.info('parse_date: parse_news: date_str: {}'.format(date_str))
            published_at = wib_to_utc(
                datetime.strptime(date_str, '%d %B %Y %H:%M'))
            loader.add_value('published_at', published_at)
        except Exception as e:
            raise CloseSpider('cannot_parse_date: {}'.format(e))

        loader.add_value('title', title)
        loader.add_value('author_name', author_name)
        loader.add_value('raw_content', raw_content)

        # Move scraped news to pipeline
        return loader.load_item()
