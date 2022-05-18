# -*- coding: utf-8 -*-
import scrapy

from gazettemachine.items import GazetteMachineItem


class SomalilandLawSpider(scrapy.Spider):
    name = 'somalilandlaw'
    allowed_domains = ['somalilandlaw.com', 'www.somalilandlaw.com']
    start_urls = ['http://www.somalilandlaw.com/somaliland_official_gazette.html']

    def parse(self, response):
        # all gazettes are on the same page and end in .pdf
        for href in response.css('a::attr(href)'):
            url = href.get()
            if url.lower().endswith('.pdf'):
                url = response.urljoin(url)
                yield GazetteMachineItem(jurisdiction='so-sl', url=url)

