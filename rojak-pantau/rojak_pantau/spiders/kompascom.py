# -*- coding: utf-8 -*-
import scrapy
import MySQLdb as mysql
import os
from datetime import datetime
from scrapy.exceptions import CloseSpider, NotConfigured
from scrapy import signals
from rojak_pantau.items import News
from scrapy.loader import ItemLoader
from slacker import Slacker

ROJAK_DB_HOST = os.getenv('ROJAK_DB_HOST', 'localhost')
ROJAK_DB_PORT = int(os.getenv('ROJAK_DB_PORT', 3306))
ROJAK_DB_USER = os.getenv('ROJAK_DB_USER', 'root')
ROJAK_DB_PASS = os.getenv('ROJAK_DB_PASS', 'rojak')
ROJAK_DB_NAME = os.getenv('ROJAK_DB_NAME', 'rojak_database')
ROJAK_SLACK_TOKEN = os.getenv('ROJAK_SLACK_TOKEN', '')

class KompasComSpider(scrapy.Spider):
	name = "kompascom"
	start_urls = [
		'http://lipsus.kompas.com/topikpilihanlist/3754/1/Pilkada.DKI.2017'
	]

	def parse(self, response):
		self.logger.info('parse web: %s' % response)
		for url in response.css("ul.clearfix > li > div.tleft > h3 > a::attr(href)").extract():
			yield scrapy.Request(url=url, callback=self.parse_news)


		next_pages = response.css("ul.paginasi.mt2 > li > a::attr(href)").extract()
		for next_url in next_pages:
			yield scrapy.Request(next_url, callback=self.parse)

	def parse_news(self, response):
		self.logger.info('parse_news: %s' % response)
		
		title = ' '.join(response.css("div.kcm-read-top > h2::text").extract())
		author_name = ' & '.join(response.css("span.pb_10::text").extract())
		raw_content = response.css("div.kcm-read-text > p").extract()
		raw_content = ' '.join(raw_content)
		date = response.css("div.kcm-date::text").extract()[0];

		loader = ItemLoader(item=News(), response=response)
		loader.add_value('url', response.url)
		loader.add_value('title', title)
		loader.add_value('author_name', author_name)
		loader.add_value('raw_content', raw_content)
		loader.add_value('url', response.url)
		loader.add_value('media_id', 1)
		loader.add_value('published_at',date)
		return loader.load_item()
