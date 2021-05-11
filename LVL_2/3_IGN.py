from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Articulo(Item):
    titulo = Field()
    contenido = Field()

class Review(Item):
    titulo = Field()
    calificacion = Field()
    
class Video(Item):
    titulo = Field()
    publicacion = Field()

class IGNCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 29 # Un poco alto
    }

    allowes_domains = ['latam.ign.com']
    download_delay = 1
    start_urls = ['https://latam.ign.com/se/?model=article&q=ps4']

    rules = (
        # TIPO DE INFORMACION
        Rule(
            LinkExtractor(
                allow = r'type='
            ),
            follow = True 
        ), 
        # PAGINACION
        Rule(
            LinkExtractor(
                allow = r'&page=\d+'
            ),
            follow = True 
        ),
        # ARTICULO
        Rule(
            LinkExtractor(
                allow = r'/news/'
            ),
            follow = True,
            callback = 'parse_news'
        ),
        # REVIEWS
        Rule(
            LinkExtractor(
                allow = r'/review/'
            ),
            follow = True,
            callback = 'parse_reviews'
        ),
        # VIDEOS
        Rule(
            LinkExtractor(
                allow = r'/videos/'
            ),
            follow=True,
            callback = 'parse_video'
        )
    )

    def parse_news(self, response):
        Item = ItemLoader(Articulo(), response)
        Item.add_xpath('titulo','//h1/text()')
        Item.add_xpath('contenido','//div[@id="id_text"]//*/text()')
        yield Item.load_item()


    def parse_review(self, response):
        Item = ItemLoader(Review(), response)
        Item.add_xpath('titulo','//h1/text()')
        Item.add_xpath('calificacion','//span[@class="side-wrapper side-wrapper hexagon-content"]/text()')
        yield Item.load_item()


    def parse_video(self, response):
        Item = ItemLoader(Video(), response)
        Item.add_xpath('titulo','//h1/text()')
        Item.add_xpath('publicacion','//span[@class="publish-date"]/text()')
        yield Item.load_item()

