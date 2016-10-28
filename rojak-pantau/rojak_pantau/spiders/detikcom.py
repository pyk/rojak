# -*- coding: utf-8 -*-
from datetime import datetime
from scrapy import Request
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
        is_no_update = False

        # Get list of news from the current page
        articles = response.css('article')
        if not articles:
            raise CloseSpider('article not found')
        for article in articles:
            # Close the spider if we don't find the list of urls
            url_selectors = article.css('a::attr(href)')
            if not url_selectors:
                raise CloseSpider('url_selectors not found')
            url = url_selectors.extract()[0]

            # Example 'detikNews | Sabtu 08 Oct 2016, 14:54 WIB'
            info_selectors = article.css('a > .text > span.info::text')
            if not info_selectors:
                raise CloseSpider('info_selectors not found')
            info = info_selectors.extract()[0]
            # Example 'Sabtu 08 Oct 2016, 14:54 WIB'
            info_time = info.split('|')[1].strip()
            # Example '08 Oct 2016, 14:54'
            info_time = ' '.join(info_time.split(' ')[1:5])

            # Parse date information
            try:
                published_at_wib = datetime.strptime(info_time,
                    '%d %b %Y, %H:%M')
            except ValueError as e:
                raise CloseSpider('cannot_parse_date: %s' % e)

            published_at = wib_to_utc(published_at_wib)

            if self.media['last_scraped_at'] >= published_at:
                is_no_update = True
                break

            # For each url we create new scrapy request
            yield Request(url + '/index?single=1', callback=self.parse_news)

        if is_no_update:
            self.logger.info('Media have no update')
            return

        if response.css('a.btn_more'):
            next_page = response.css('a.btn_more::attr(href)')[0].extract()
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse)
        elif response.css('div.pag-nextprev > a'):
            next_page = response.css('div.pag-nextprev > a::attr(href)')[1].extract()
            next_page_url = response.urljoin(next_page)
            yield Request(next_page_url, callback=self.parse)

    def parse_multipage_content(self, response):
        loader = response.meta['loader']
        n = response.meta['n']

        xpath_query = """
            //div[@class="text_detail"]/node()
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

        # Get page number
        # Example: http://m.detik.com/news/berita/d-3302845/balada-kencan-singkat-ahok-heru/3
        page = response.url[response.url.rindex('/')+1:]
        loader.add_value('raw_content', {'page': page, 'content': raw_content})

        rc = loader.get_collected_values('raw_content')

        # when we get all the pages, concatenate the parts into raw_content
        if len(rc) == n:
            rc.sort(key=lambda x: x['page'])
            raw_content = ''.join(map(lambda x: x['content'], rc))
            loader.replace_value('raw_content', raw_content)
            return loader.load_item()

    def parse_indices(self, indices, loader):
        for index in indices:
            yield Request(index, meta={'loader': loader, 'n': len(indices)},
                    callback=self.parse_multipage_content)

    # Collect news item
    def parse_news(self, response):
        self.logger.info('parse_news: %s' % response)

        # Initialize item loader
        # extract news title, published_at, author, content, url
        # Required: title, raw_content, published_at
        loader = ItemLoader(item=News(), response=response)
        loader.add_value('url', response.url)
        title_selectors = response.css('div.detail_area > h1.jdl::text')
        if not title_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()
        title = title_selectors.extract()[0]
        loader.add_value('title', title)

        # Parse date information
        # Example: Kamis 15 Sep 2016, 18:33 WIB
        date_selectors = response.css('div.detail_area > div.date::text')
        if not date_selectors:
            # Will be dropped on the item pipeline
            return loader.load_item()

        date_str = date_selectors.extract()[0]
        # Example: '15 Sep 2016, 18:33'
        date_str = ' '.join(date_str.split(' ')[1:5])
        try:
            published_at_wib = datetime.strptime(date_str, '%d %b %Y, %H:%M')
        except ValueError:
            # Will be dropped on the item pipeline
            return loader.load_item()

        published_at = wib_to_utc(published_at_wib)
        loader.add_value('published_at', published_at)

        author_name_selectors = response.css('div.author > strong::text')
        if not author_name_selectors:
            loader.add_value('author_name', '')
        else:
            author_name = author_name_selectors.extract()[0]
            loader.add_value('author_name', author_name)

        # Check for multipage
        xpath_query = "//div[@class='list_multi']/article/a/@href"
        multipage_selectors = response.xpath(xpath_query)
        if multipage_selectors:
            indices = ['http:' + x for x in multipage_selectors.extract()]
            return self.parse_indices(indices, loader)

        # Extract the content using XPath instead of CSS selector
        # We get the XPath from chrome developer tools (copy XPath)
        # or equivalent tools from other browser
        xpath_query = """
            //div[@class="text_detail detail_area"]/node()
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

        # Move scraped news to pipeline
        return loader.load_item()
