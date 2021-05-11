from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

class TripAdvisorSpider(CrawlSpider):
    name = 'TripAdvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']
    
    download_delay = 2

    rules = (
        Rule(
            LinkExtractor(
                allow = r'Hotel_Review-'
            ), 
            follow = True,
            callback = 'parse_hotel'
        )
    )

    def parse_hotel(self, response):
        selector = Selector(response)
        item = ItemLoader(Hotel(),selector)
        item.add_xpath('nombre','//h1[@id="HEADING"]/text()')
        # item.add_xpath('precio','//div[@class="_2Ngw5d8g"]/div[@class="ui_columns"]/div[@class="_1j6xaJwD"]/div[@class="_3kGtuPhC"]/div[@class="_36QMXqQj"]/text()')     
        # item.add_xpath('descripcion', '//div[@class="hotels-hotel-offers-DominatOffer__price--D-ycN"]/text()')
        item.add_xpath('descripcion', '//div[contains(@class, "hotel-review-about-csr-Description__description")]/div/text()',
        MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities', '//div[contains(@class, "hotels-hr-about-amenities-Amenity__amenity--3fbBj")]/text()')
        yield item.load_item()

# scrapy runspider .\3_STACKOVERFLOW-SCRAPY.py -o archivo.csv -t csv RUN SCRAPY

# /html/body/div[2]/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[6]/div/div/div[1]/div[3]/div[1]/div[2]/div/div[2]