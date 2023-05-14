import scrapy
import datetime

from gazettemachine.items import GazetteMachineItem


class SeychellesSpider(scrapy.Spider):
    name = 'seychelles'
    allowed_domains = ['gazette.sc', 'www.gazette.sc']

    def start_requests(self):
        for year in range(2023, datetime.date.today().year + 1):
            yield scrapy.Request(f'https://www.gazette.sc/v/gazette/{year}', self.parse)
            yield scrapy.Request(f'https://www.gazette.sc/v/act/{year}', self.parse)
            yield scrapy.Request(f'https://www.gazette.sc/v/si/{year}', self.parse)
            yield scrapy.Request(f'https://www.gazette.sc/v/bill/{year}', self.parse)

    def parse(self, response):
        for href in response.css('div.views-infinite-scroll-content-wrapper div.views-field-nothing a::attr(href)'):
            url = href.get()
            if url.lower().endswith('.pdf'):
                url = response.urljoin(url)
                yield GazetteMachineItem(jurisdiction='sc', url=url)

        next_page = response.css('li.pager__item a::attr(href)')
        if next_page:
            for href in response.css('li.pager__item a::attr(href)'):
                url = href.get()
                if "?search=&no=&page" in url:
                    yield response.follow(href, self.parse)

