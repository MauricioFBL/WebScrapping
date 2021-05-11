from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup

class Pregunta(Item):
    id = Field()
    pregunta = Field()
    # descripcion = Field()

class StackOverflowSpider(Spider):
    name = 'MiPrimerSPIDER'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    # URL SEMILLA
    start_urls = ['https://stackoverflow.com/questions']

    def parse(self, response):
        selector = Selector(response)
        preguntas = selector.xpath('//div[@id="questions"]//div[@class="question-summary"]')
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta)
            item.add_xpath('pregunta','.//h3/a/text()')
            # item.add_xpath('descripcion','.//div[@class="excerpt"]/text()')
            item.add_value('id',1)
            yield item.load_item()

# scrapy runspider .\3_STACKOVERFLOW-SCRAPY.py -o archivo.csv -t csv RUN SCRAPY