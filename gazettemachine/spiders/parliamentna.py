# -*- coding: utf-8 -*-
import scrapy


from gazettemachine.items import GazetteMachineItem


class ParliamentnaSpider(scrapy.Spider):
    name = 'parliamentna'
    allowed_domains = ['laws.parliament.na']
    start_urls = ['https://laws.parliament.na/gazettes/namibia-government-gazettes.php?id=1']

    def parse(self, response):
        for href in response.css('table.page-content-table td:first-child a::attr(href)'):
            yield response.follow(href, self.parse_listing)

    def parse_listing(self, response):
        for href in response.css('table.page-content-table td:first-child a::attr(href)'):
            yield GazetteMachineItem(jurisdiction='na', url=href.extract())
