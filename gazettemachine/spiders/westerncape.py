import scrapy
import datetime

from gazettemachine.items import GazetteMachineItem


class WesternCapeSpider(scrapy.Spider):
    name = 'westerncape'
    allowed_domains = ['westerncape.gov.za']

    def start_requests(self):
        for year in range(2024, datetime.date.today().year + 1):
            # pre 2024 at https://www.westerncape.gov.za/general-publication/provincial-gazettes-YYYY
            # 2024 at     https://www.westerncape.gov.za/general-publication/provincial-gazette-YYYY
            yield scrapy.Request(f'https://www.westerncape.gov.za/general-publication/provincial-gazette-{year}', self.parse_pg_listing)

    def parse_pg_listing(self, response):
        for href in response.css('div.node-wcg-general-publication ul li a::attr(href)'):
            url = href.get()
            if url.lower().endswith('.pdf'):
                url = response.urljoin(url)
                yield GazetteMachineItem(jurisdiction='za-wc', url=url)
            else:
                yield response.follow(href, self.parse_pg_listing)
