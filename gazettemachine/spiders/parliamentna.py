# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import scrapy


from gazettemachine.items import GazetteMachineItem


class ParliamentnaSpider(scrapy.Spider):
    name = 'parliamentna'
    allowed_domains = ['laws.parliament.na']
    start_urls = ['https://laws.parliament.na/gazettes/namibia-government-gazettes.php?id=1']

    def parse(self, response):
        for href in response.css('table.page-content-table td:first-child a::attr(href)'):
            yield response.follow(href, self.parse_main_listing)

    def parse_main_listing(self, response):
        if response.css('#loadmore-gazette'):
            parsed = urlparse.urlparse(response.url)
            year = int(urlparse.parse_qs(parsed.query)['y'][0])
            yield response.follow('https://laws.parliament.na/ajax/ajax.fetchGazettes.php?id=1&y=%s&page=2' % year,
                                  self.parse_partial_listing,
                                  meta={'year': year, 'page': 2})

        for href in response.css('table.page-content-table td:first-child a::attr(href)'):
            yield GazetteMachineItem(jurisdiction='na', url=href.extract())

    def parse_partial_listing(self, response):
        if response.body.strip():
            # probably another page
            page = response.meta['page'] + 1
            year = response.meta['year']
            yield response.follow('https://laws.parliament.na/ajax/ajax.fetchGazettes.php?id=1&y=%s&page=%s' % (year, page),
                                  self.parse_partial_listing,
                                  meta={'year': response.meta['year'], 'page': page})

        for href in response.css('td:first-child a::attr(href)'):
            yield GazetteMachineItem(jurisdiction='na', url=href.extract())
