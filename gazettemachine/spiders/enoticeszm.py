# -*- coding: utf-8 -*-
import re
import scrapy


from gazettemachine.items import GazetteMachineItem

href_re = re.compile(r"href='([^'&]+)")


class EnoticesZMSpider(scrapy.Spider):
    name = 'enoticeszm'
    allowed_domains = ['www.enotices.co.zm']
    start_urls = ['https://www.enotices.co.zm/categories/government-gazettes/']

    def parse(self, response):
        for href in response.css('.content a.en_category_box::attr(href)'):
            url = response.urljoin(href.get())
            yield scrapy.Request(url, self.parse_listing)

    def parse_listing(self, response):
        for onclick in response.css('#wpdm-all-packages a.wpdm-download-link::attr(onclick)'):
            # suck out the location
            # onclick="location.href='https://www.enotices.co.zm/download/government-gazette-no-01-of-lusaka-5th-january-2016-pdf/?wpdmdl=1679&refresh=5e676e5245b211583836754';return false;"
            match = href_re.search(onclick.get())
            if match:
                url = match.group(1)
                yield GazetteMachineItem(jurisdiction='zm', url=url)
