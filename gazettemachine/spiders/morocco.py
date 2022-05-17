# -*- coding: utf-8 -*-
import scrapy
import time
import json

from gazettemachine.items import GazetteMachineItem


class MoroccoSpider(scrapy.Spider):
    name = 'morocco'
    allowed_domains = ['sgg.gov.ma', 'www.sgg.gov.ma']
    start_urls = ['http://www.sgg.gov.ma/BulletinOfficiel.aspx']

    def current_time_in_ms(self):
        return round(time.time() * 1000)

    def parse(self, response):
        rv_token = response.css("input[name='__RequestVerificationToken']::attr(value)").extract_first()

        # The start url gives us the page with the request verification token and is also used as referrer by scrapy.FormRequest
        yield scrapy.FormRequest(
                f'http://www.sgg.gov.ma/DesktopModules/MVC/TableListBO/BO/AjaxMethod?_={self.current_time_in_ms()}',
                headers={
                    'ModuleId': '2873',
                    'TabId': '775',
                    '__RequestVerificationToken': rv_token,
                },
                callback=self.parse_json
            )

    def parse_json(self, response):
        """ The list of gazettes is send back in JSON.

        Sample JSON: [
            {'BoId': 12540, 'BoNum': '7070', 'BoDate': '/Date(1646262000000)/', 'BoUrl': 'http://www.sgg.gov.ma/BO/FR/2873/2022/BO_7070_Fr.pdf'},
            {'BoId': 12555, 'BoNum': '7074', 'BoDate': '/Date(1647385200000)/', 'BoUrl': 'http://www.sgg.gov.ma/BO/FR/2873/2022/BO_7074 _Fr.pdf'}
        ]
        """
        gazettes = json.loads(response.text)
        for i in gazettes:
            if i.get('BoUrl'):
                yield GazetteMachineItem(jurisdiction='ma', url=i.get('BoUrl'))
