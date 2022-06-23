# -*- coding: utf-8 -*-
import re
import scrapy


postid_re = re.compile(r"postid-(\d+)")


class EnoticesZMSISpider(scrapy.Spider):
    name = 'enoticeszm_si'
    allowed_domains = ['www.enotices.co.zm']
    start_urls = ['https://www.enotices.co.zm/categories/statutory-instruments/']

    def parse(self, response):

        for a in response.css('.content a.en_category_box'):
            url = response.urljoin(a.attrib['href'])
            title = ''.join(a.xpath('.//h4//text()').getall())
            year = title.split(' ')[-1]
            yield scrapy.Request(url, self.parse_listing, cb_kwargs={'year': year})

    def parse_listing(self, response, year):
        for a in response.css('#wpdm-all-packages a.package-title'):
            url = a.attrib['href']
            title = ''.join(a.xpath('.//text()').getall())
            yield scrapy.Request(url, self.parse_detail, cb_kwargs={'year': year, 'title': title})

    def parse_detail(self, response, year, title):
        for cls in response.css('body::attr(class)'):
            m = postid_re.search(cls.get())
            if m:
                url = 'https://www.enotices.co.zm/?wpdmdl=' + m.group(1)
                yield {'url': url, 'year': year, 'title': title}
