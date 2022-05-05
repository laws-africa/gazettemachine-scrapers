# -*- coding: utf-8 -*-
import scrapy

from gazettemachine.items import GazetteMachineItem


class GovRWSpider(scrapy.Spider):
    name = 'govrw'
    allowed_domains = ['minijust.gov.rw', 'www.minijust.gov.rw']
    start_urls = ['https://www.minijust.gov.rw/official-gazette']

    def parse(self, response):
        # year, month and gazette listing pages all have the same format
        for href in response.css('.tx-filelist table td a::attr(href)'):
            url = href.get()

            # base file URL https://www.minijust.gov.rw/index.php?eID=dumpFile&t=f&f=31203&token=...
            if 'index.php?eID=dumpFile&t=f' in url:
                url = response.urljoin(url)
                yield GazetteMachineItem(jurisdiction='rw', url=url)
            else:
                yield response.follow(href, self.parse)
