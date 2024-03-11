import scrapy

from gazettemachine.items import GazetteMachineItem


class UtumishiTZSpider(scrapy.Spider):
    name = 'utumishitz'
    allowed_domains = ['www.utumishi.go.tz']
    start_urls = ['https://www.utumishi.go.tz/documents/government-gazette']

    def parse(self, response):
        for href in response.css('.page-content .document-card-list-item a::attr(href)'):
            url = response.urljoin(href.get())
            yield GazetteMachineItem(jurisdiction='tz', url=url)
