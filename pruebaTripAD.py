from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    amenities = Field()

class TripSpider(Spider):
    name = 'MiPrimerSPIDER'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
    # URL SEMILLA
    start_urls = ['https://www.tripadvisor.com.mx/Hotel_Review-g303845-d6527792-Reviews-Iguanazu_Bed_Breakfast-Guayaquil_Guayas_Province.html']
    # Funcion a utilizar con MapCompose para realizar limpieza de datos
    
    def quitarDolar(self, texto):
        return texto.replace("$", "")

    def parse(self, response):
        selector = Selector(response)
        item = ItemLoader(Hotel(),selector)
        item.add_xpath('nombre','//h1[@id="HEADING"]/text()')
        # item.add_xpath('precio','(//div[@class="_36QMXqQj"])[last()]/text()')
        item.add_xpath('precio', './/div[@class="hotels-hotel-offers-DominantOffer__price--D-ycN"]/text()',MapCompose(self.quitarDolar))
        # Utilizo Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas en Python?
        item.add_xpath('descripcion', '//div[contains(@class, "hotel-review-about-csr-Description__description")]/div/text()',MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities','//div[contains(@class, "hotels-hr-about-amenities-Amenity__amenity--3fbBj")]/text()')
        
        # item.add_xpath('precio','//div[@class="_36QMXqQj"]/text()[last()]')
        # item.add_xpath('precio','//div[@class="meta_inner"]//div[@class="_2Ngw5d8g"]//div[@class="ui_columns"]//div[@class="_1j6xaJwD"]//div[@class="_3kGtuPhC"]//div[@class="_36QMXqQj"]/text()')
        yield item.load_item()
        
# scrapy runspider .\3_STACKOVERFLOW-SCRAPY.py -o archivo.csv -t csv RUN SCRAPY