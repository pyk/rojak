# -*- coding: utf-8 -*-
import scrapy


class DetikcomSpider(scrapy.Spider):
    name = "detikcom"
    allowed_domains = ["detik.com"]
    start_urls = (
        'http://m.detik.com/news/indeksfokus/67/jakarta-memilih',
    )

    def parse(self, response):
        print '== DEBUG:', response
        pass
