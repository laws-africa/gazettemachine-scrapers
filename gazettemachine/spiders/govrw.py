# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import scrapy
import datetime


from gazettemachine.items import GazetteMachineItem


class GovRWSpider(scrapy.Spider):
    name = 'govrw'
    allowed_domains = ['minijust.gov.rw', 'www.minijust.gov.rw']
    start_urls = ['https://www.minijust.gov.rw/official-gazette']

    def parse(self, response):
        # year, month and gazette listing pages all have the same format
        for href in response.css('.tx-filelist table td a::attr(href)'):
            url = href.get()
            if url.lower().endswith('.pdf'):
                url = response.urljoin(url)
                yield GazetteMachineItem(jurisdiction='rw', url=url)
            else:
                yield response.follow(href, self.parse)
