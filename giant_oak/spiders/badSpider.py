from urllib.parse import urljoin
import scrapy
from ..items import ProfileItem
from scrapy.loader import ItemLoader

class badSpider(scrapy.Spider):
    name = 'bad_guys'
    start_urls = [
        'https://www.nationalcrimeagency.gov.uk/most-wanted-search'
    ]

    def parse(self, response):
        yield {
            'source_code': 'giant_oak',
        }
        yield {
            'source_name': 'National Crime Agency',
        }
        yield {
            'source_url': 'https://www.nationalcrimeagency.gov.uk/most-wanted-search'
        }
        links = (response.xpath("//div[@class='pull-none item-image']//a/@href").getall())
        for link in links:
            url = urljoin('https://www.nationalcrimeagency.gov.uk/most-wanted-search', link)
            print(link)
            request = scrapy.Request(url, callback=self.parse_link)
            yield request


    def parse_link(self, response):
        profile = ProfileItem()
        person = dict()
        unclean_name = response.xpath('//*[@id="content"]/div/div[3]/div[1]/h2/text()').extract_first()
        name = unclean_name[5:-3]
        person['name'] = name

        div_num = 0
        for div_object in response.xpath('//*[@id="content"]/div/div[3]/div[5]/div'):
            div_num += 1
            span_num = 0
            for span_object in response.xpath(f'//*[@id="content"]/div/div[3]/div[5]/div[{div_num}]/span'):
                span_num += 1
                entity_name = span_object.xpath(f'//*[@id="content"]/div/div[3]/div[5]/div[1]/span[{span_num}]/text()').extract_first()
                if entity_name is None:
                    break
                span_num += 1
                entity_body = span_object.xpath(f'//*[@id="content"]/div/div[3]/div[5]/div[1]/span[{span_num}]/text()').extract_first()
                person[f"{entity_name}"] = entity_body
        profile['person'] = person
        yield profile



