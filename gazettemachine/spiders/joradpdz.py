import scrapy
import datetime


from gazettemachine.items import GazetteMachineItem


class JoradpdzScraper(scrapy.Spider):
    name = 'joradpdz'
    allowed_domains = ['joradp.dz']

    def start_requests(self):
        # years
        # TODO: once deployed and run once, only do this year and next year
        current_year = datetime.date.today().year
        for year in range(current_year, current_year + 2):
            yield scrapy.Request(f'https://www.joradp.dz/JRN/ZF{year}.htm', self.parse_listing,
                                 cb_kwargs={'year': year})

    def parse_listing(self, response, year):
        for opt in response.css('form[name="zFrm2"] select[name="znjo"] > option[value]'):
            try:
                num = int(opt.attrib['value'])
            except ValueError:
                continue

            yield GazetteMachineItem(
                jurisdiction='dz',
                url=f'https://www.joradp.dz/FTP/JO-FRANCAIS/{year}/F{year}{num:03}.pdf')
