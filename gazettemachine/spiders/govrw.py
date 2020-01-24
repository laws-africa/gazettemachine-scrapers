# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import scrapy
import datetime


from gazettemachine.items import GazetteMachineItem


class GovRWSpider(scrapy.Spider):
    name = 'govrw'
    allowed_domains = ['minijust.gov.rw', 'www.minijust.gov.rw']
    start_urls = ['https://www.minijust.gov.rw/index.php?id=133']

    def parse(self, response):
        # paginator
        for href in response.css('.page-navigation .pagination li a::attr(href)'):
            yield response.follow(href, self.parse)

        # gazettes
        for href in response.css('.news li a::attr(href)'):
            href = href.get()
            if href.lower().endswith('.pdf'):
                yield GazetteMachineItem(jurisdiction='rw', url=href)
