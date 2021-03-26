from urllib.parse import urljoin
import scrapy
from ..items import ProfileItem

class badSpider(scrapy.Spider):
    name = 'bad_guys'

    #source url
    start_urls = [
        'https://www.nationalcrimeagency.gov.uk/most-wanted-search'
    ]


    def parse(self, response):

        # Establish source code, source name and the source url for the JSON file
        yield {
            'source_code': 'giant_oak',
        }
        yield {
            'source_name': 'National Crime Agency',
        }
        yield {
            'source_url': 'https://www.nationalcrimeagency.gov.uk/most-wanted-search'
        }

        #Grab links to individual profiles of each criminal
        links = (response.xpath("//div[@class='pull-none item-image']//a/@href").getall())

        for link in links:
            #Take original link and concatenate profile stub to get url for individual profile
            url = urljoin('https://www.nationalcrimeagency.gov.uk/most-wanted-search', link)

            #Parse inside of each criminal profile using seperate parse method using our concatenated link
            request = scrapy.Request(url, callback=self.parse_link)

            #Return all information retrieved from parse_link
            yield request


    def parse_link(self, response):

        #ProfileItem contains data on single criminal
        profile = ProfileItem()
        person = dict()

        #Since there is always a name, we grab it first and get rid of the HTML tags and create a name mapping
        #in the profile dictionary
        unclean_name = response.xpath('//*[@id="content"]/div/div[3]/div[1]/h2/text()').extract_first()
        split_name = unclean_name[5:-3].split()
        first_name = split_name[0]
        last_name = split_name[1]
        person['First name'] = first_name
        person['Last name'] = last_name

        div_num = 1
        span_num = 0

        about = dict()

        # There are three divs in each profile, with variable amounts of spans which contain data
        while div_num < 4:
            for span_object in response.xpath(f'//*[@id="content"]/div/div[3]/div[5]/div'):
                span_num += 1

                #Grab first span which contains the data identity
                entity_name = response.xpath(f'//*[@id="content"]/div/div[3]/div[5]/div[{div_num}]/span[{span_num}]/text()').extract_first()

                #prevents yielding of null JSON properties relating to parsing span which don't exist
                if entity_name is None:
                    break
                span_num += 1

                #Grab partner span which contains the data relating to the identity
                entity_body = span_object.xpath(f'//*[@id="content"]/div/div[3]/div[5]/div[{div_num}]/span[{span_num}]/text()').extract_first()
                about[f"{entity_name}"] = entity_body
            span_num = 0
            div_num += 1

        #Set JSON object equal to person dictionary containing individual information
        person['about'] = about
        profile['person'] = person

        #Return criminals profile in JSON to data.json
        yield profile



