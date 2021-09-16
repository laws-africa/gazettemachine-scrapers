# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import scrapy


from gazettemachine.items import GazetteMachineItem


class WesternCapeSpider(scrapy.Spider):
    name = 'westerncape'
    allowed_domains = ['westerncape.gov.za']
    start_urls = [
        'https://www.westerncape.gov.za/general-publication/provincial-gazettes-2021',
    ]

    def parse(self, response):
        for href in response.css('div.node-wcg-general-publication ul li a::attr(href)'):
            url = href.get()
            if url.lower().endswith('.pdf'):
                url = response.urljoin(url)
                yield GazetteMachineItem(jurisdiction='za-wc', url=url)
            else:
                yield response.follow(href, self.parse)
