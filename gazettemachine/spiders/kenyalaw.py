# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import scrapy
import datetime


from gazettemachine.items import GazetteMachineItem


class KenyalawSpider(scrapy.Spider):
    name = 'kenyalaw'
    allowed_domains = ['kenyalaw.org', 'www.kenyalaw.org']

    def start_requests(self):
        # KG
        for year in range(2024, datetime.date.today().year + 1):
            pass
            #yield scrapy.Request(f'http://www.kenyalaw.org/kenya_gazette/gazette/year/{year}/', self.parse_kg_listing)

        # KGS
        # 2021
        # 2022
        # 2023
        # 2024
        for nid in ['11363', '11550', '11741', '12002']:
            yield scrapy.Request(f'http://kenyalaw.org/kl/index.php?id={nid}', self.parse_kgs_listing)

    def parse_kg_listing(self, response):
        for href in response.css('.page-content .gazette-content table td:nth-child(2) a::attr(href)'):
            yield response.follow(href, self.parse_kg_page)

    def parse_kg_page(self, response):
        for href in response.css('.gazette-content .sd a::attr(href)'):
            href = href.get()
            if href.lower().endswith('.pdf'):
                url = response.urljoin(href)
                yield GazetteMachineItem(jurisdiction='ke', url=url)

    def parse_kgs_listing(self, response):
        for href in response.css('.contenttable a::attr(href)'):
            href = href.get()
            if href.lower().endswith('.pdf'):
                url = response.urljoin(href)
                yield GazetteMachineItem(jurisdiction='ke', url=url)
