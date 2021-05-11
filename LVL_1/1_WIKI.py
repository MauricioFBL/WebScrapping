import requests
from lxml import html

url = "https://es.wikipedia.org/wiki/Wikipedia:Portada"

# USER AGENT PARA EVITAR BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}
# URL PAGINA CRAWLEO 
url = 'https://www.wikipedia.org/'

# REQUERIMIENTOS
respuesta = requests.get(url, headers =  headers)
# print(respuesta.text)

# PARSEO DE HTML COMO LXML
parser = html.fromstring(respuesta.text)

#EXTRCCION DEL IDIOMA INGLES
ingles = parser.get_element_by_id("js-link-box-en")
print(ingles.text_content())

# EXTRACCION DEL TEXTO QUE DICE INGLES XPATH
ingles = parser.xpath("//a[@id='js-link-box-en']/strong/text()")

# EXTRACCION DE TODOS POR XPATH
idiomas = parser.xpath("//div[contains(@class,'central-featured-lang')]//strong/text()")
for idioma in idiomas:
    print(idioma)
    
# EXTRACCION DE TODOS POR CLASE
idiomas = parser.find_class('central-featured-lang')
for idioma in idiomas:
    print(idioma.text_content())

print('XPATH')



