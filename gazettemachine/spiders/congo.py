import scrapy
import datetime

from gazettemachine.items import GazetteMachineItem


class CongoSpider(scrapy.Spider):
    name = 'congo'
    allowed_domains = ['sgg.cg']

    def start_requests(self):
        yield scrapy.Request('https://www.sgg.cg/fr/journal-officiel/le-journal-officiel.html', self.parse)
        yield scrapy.Request('https://www.sgg.cg/1/146/fr/journal-officiel/journaux-speciaux.html?page=0', self.parse)

    def parse(self, response):
        for href in response.css('.search-results .card-content a.link-jo::attr(href)'):
            url = href.get()
            if url.lower().endswith('.pdf'):
                url = response.urljoin(url)
                yield GazetteMachineItem(jurisdiction='cg', url=url)
