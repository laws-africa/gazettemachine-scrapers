# -*- coding: utf-8 -*-
import urllib.parse as urlparse
import scrapy

from gazettemachine.items import GazetteMachineItem


class GPWSpider(scrapy.Spider):
    name = 'gpw'
    allowed_domains = ["gpwonline.co.za", "gpwonline.sharepoint.com"]
    # ZA use sharepoint, which requires different auth for each different list
    # pairs of auth-url, data url
    national_gazette_urls = [
        (
            # national
            "https://gpwonline.sharepoint.com/:f:/s/gpw-web/EhxpblSM5NpCh_N3xAZ6rukB6dTsdHf3ZZJKYh0Pa8J9iA?e=Mc3e73",
            "https://gpwonline.sharepoint.com/sites/gpw-web/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1=%27%2Fsites%2Fgpw%2Dweb%2FShared%20Documents%27&RootFolder=%2Fsites%2Fgpw%2Dweb%2FShared%20Documents%2FGovernment&View=7a8fe278-931f-49d0-9374-c8d511d7c610&SortField=PublicationDte&SortDir=Desc&TryNewExperienceSingle=TRUE"
        ),
        (
            # legal#
            "https://gpwonline.sharepoint.com/:f:/s/gpw-web/EuUVRm9dXElCjAXBiPdf2xgBAbjuQaq_s8j9c8x7qbVFzg?e=ZCkbyO",
            "https://gpwonline.sharepoint.com/sites/gpw-web/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1=%27%2Fsites%2Fgpw%2Dweb%2FShared%20Documents%27&RootFolder=%2Fsites%2Fgpw%2Dweb%2FShared%20Documents%2FLegal&View=7a8fe278-931f-49d0-9374-c8d511d7c610&SortField=PublicationDte&SortDir=Desc&TryNewExperienceSingle=TRUE"
        ),
        (
            # acts
            "https://gpwonline.sharepoint.com/:f:/s/gpw-web/EooEacaIkXZHtl0ZxDAC5aEBqhpN139p3l0jNC-9n6VSNw?e=E2VTxS",
            "https://gpwonline.sharepoint.com/sites/gpw-web/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1=%27%2Fsites%2Fgpw%2Dweb%2FShared%20Documents%27&RootFolder=%2Fsites%2Fgpw%2Dweb%2FShared%20Documents%2FActs&View=7a8fe278-931f-49d0-9374-c8d511d7c610&SortField=PublicationDte&SortDir=Desc&TryNewExperienceSingle=TRUE"
        )
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
        # start by getting and storing an auth cookie
        for i, (auth_url, list_url) in enumerate(self.national_gazette_urls):
            yield scrapy.Request(auth_url, self.authenticated, cb_kwargs={'list_url': list_url}, meta={'cookiejar': i})

    def authenticated(self, response, list_url):
        # now start the actual crawling
        headers = {
            'authority': 'gpwonline.sharepoint.com',
            'accept': 'application/json;odata=verbose',
            'accept-language': 'en-US',
            'application': 'sp_files',
            'content-type': 'application/json;odata=verbose',
            'origin': 'https://gpwonline.sharepoint.com',
            'scenario': 'ViewList',
            'scenariotype': 'AUO',
            'x-clientservice-clienttag': 'SPList Web',
            'x-sp-requestresources': 'listUrl=%2Fsites%2Fgpw%2Dweb%2FShared%20Documents',
        }

        body = '{"parameters":{"__metadata":{"type":"SP.RenderListDataParameters"},"RenderOptions":1445895,"AllowMultipleValueFilterForTaxonomyFields":true,"AddRequiredFields":true,"FilterOutChannelFoldersInDefaultDocLib":true}}'
        yield scrapy.Request(list_url, self.parse, headers=headers, body=body, method="POST",
                             meta={'cookiejar': response.meta['cookiejar']})

    def parse(self, response):
        for row in response.json()['ListData']['Row']:
            url = f"https://gpwonline.sharepoint.com/sites/gpw-web/_layouts/15/download.aspx?SourceUrl={row['FileRef.urlencode']}"
            yield GazetteMachineItem(jurisdiction='za', url=url)
