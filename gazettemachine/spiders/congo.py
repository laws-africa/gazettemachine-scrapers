# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import scrapy
import datetime

from gazettemachine.items import GazetteMachineItem


class CongoSpider(scrapy.Spider):
    name = 'congo'
    allowed_domains = ['sgg.cg']

    def start_requests(self):
        yield scrapy.Request('https://www.sgg.cg/fr/journal-officiel/le-journal-officiel.html', self.parse_ordinary)
        yield scrapy.Request('https://www.sgg.cg/1/146/fr/journal-officiel/journaux-speciaux.html?page=0', self.parse_special)

    def parse_ordinary(self, response):
        for year in range(2020, datetime.date.today().year + 1):
            css_string = f'ul#jos_{year} li#bloc_{year} a::attr(href)'
            for href in response.css(css_string):
                url = href.get()
                if url.lower().endswith('.pdf'):
                    url = response.urljoin(url)
                    yield GazetteMachineItem(jurisdiction='cg', url=url)

    def parse_special(self, response):
        for href in response.css('div.collection.jos h4.titre_annee a::attr(href)'):
            url = href.get()
            if url.lower().endswith('.pdf'):
                url = response.urljoin(url)
                yield GazetteMachineItem(jurisdiction='cg', url=url)
