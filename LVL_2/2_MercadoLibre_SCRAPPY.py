from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Producto(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()

class MercadoLibreSpider(CrawlSpider):
    name = 'MercadoLibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20 # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero
    }
    download_delay = 1
    allowed_domains = ['articulo.mercadolibre.com.mx', 'listado.mercadolibre.com.mx']
    start_urls = ['https://videojuegos.mercadolibre.com.mx/videojuegos/xbox-one/']

    rules = (
        # REGLA DE PAGINACION
        Rule(
            LinkExtractor(
                allow = r'/_Desde_'
            ),
            follow = True
        ),
        # REGLA DE DETALLE PRODUCTO
        Rule(
            LinkExtractor(
                allow = r'/MLM-'
            ),
            follow = True,
            callback='parse_items'
        ),
    )

    def limpiartTexto(self, texto):
        nuevoTexto = texto.replace('\n','').replace('\r','').replace('\t','').strip()
        return nuevoTexto

    def parse_items(self, response):
        item = ItemLoader(Producto(), response)

        item.add_xpath('nombre', '//h1/text()', MapCompose(self.limpiartTexto))
        item.add_xpath('precio', '//span[@class="price-tag-fraction"]/text()')
        # response.xpath('//span[@class="price-tag-fraction"]/text()')
        item.add_xpath('descripcion','//div[@class="ui-pdp-description"]/p/text()',MapCompose(self.limpiartTexto))
        yield item.load_item()
        # scrapy.exe runspider x.py -o VideojuegosMlibre.csv -t csv