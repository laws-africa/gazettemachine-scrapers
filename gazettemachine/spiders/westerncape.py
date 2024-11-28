import scrapy
import datetime

from gazettemachine.items import GazetteMachineItem


class WesternCapeSpider(scrapy.Spider):
    name = 'westerncape'
    allowed_domains = ['westerncape.gov.za']

    def start_requests(self):
        for year in range(2024, datetime.date.today().year + 1):
            # pre 2024 at https://d7.westerncape.gov.za/general-publication/provincial-gazettes-YYYY
            # 2024 at     https://d7.westerncape.gov.za/general-publication/provincial-gazette-YYYY
            # go back three months
            for i in [1, 2, 3]:
                yield scrapy.Request(f'https://d7.westerncape.gov.za/general-publication/provincial-gazette-{year}?toc_page={i}', self.parse_pg_listing)

    def parse_pg_listing(self, response):
        for href in response.css('.node-wcg-general-publication .field-items ul li a::attr(href)'):
            url = href.get()
            if url.lower().endswith('.pdf'):
                url = response.urljoin(url)
                # change www to d7
                url = url.replace('www.westerncape.gov.za', 'd7.westerncape.gov.za')
                yield GazetteMachineItem(jurisdiction='za-wc', url=url)
