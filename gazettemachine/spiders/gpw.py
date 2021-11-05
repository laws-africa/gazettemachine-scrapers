# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import scrapy

from gazettemachine.items import GazetteMachineItem


class GPWSpider(scrapy.Spider):
    name = 'gpw'
    allowed_domains = ["gpwonline.co.za"]
    national_gazette_urls = [
        'http://www.gpwonline.co.za/Gazettes/Pages/Published-Legal-Gazettes.aspx',
        'http://www.gpwonline.co.za/Gazettes/Pages/Published-Liquor-Licenses.aspx',
        'http://www.gpwonline.co.za/Gazettes/Pages/Published-National-Government-Gazettes.aspx',
        'http://www.gpwonline.co.za/Gazettes/Pages/Published-National-Regulation-Gazettes.aspx',
        'http://www.gpwonline.co.za/Gazettes/Pages/Published-Separate-Gazettes.aspx',
        'http://www.gpwonline.co.za/Gazettes/Pages/Published-Tender-Bulletin.aspx',
        'http://www.gpwonline.co.za/Gazettes/Pages/Road-Access-Permits.aspx',
    ]
    jurisdictions = {
        "za-ec": "Eastern-Cape",
        "za-gt": "Gauteng",
        "za-kzn": "KwaZulu-Natal",
        "za-lim": "Limpopo",
        "za-mp": "Mpumalanga",
        "za-nw": "North-West",
        "za-nc": "Northern-Cape",
    }

    def start_requests(self):
        for url in self.national_gazette_urls:
            yield scrapy.Request(url, self.parse, cb_kwargs={'code': 'za'})

        for code, jurisdiction in self.jurisdictions.items():
            yield scrapy.Request(f'http://www.gpwonline.co.za/Gazettes/Pages/Provincial-Gazettes-{jurisdiction}.aspx', self.parse, cb_kwargs={'code': code})

    def parse(self, response, code):
        for row in response.css('div.GazetteTitle'):
            href = row.css('div a::attr(href)').get()
            if href.lower().endswith('.pdf'):
                url = response.urljoin(href)
                yield GazetteMachineItem(jurisdiction=code, url=url)

        next_page_xpath = '//div[@class="Paging"]/div/strong/following-sibling::a/@href'
        next_pages = response.xpath(next_page_xpath)
        if next_pages:
            yield scrapy.Request(urlparse.urljoin(response.url, next_pages[0].extract()), cb_kwargs={'code': code})
