import requests
from bs4 import BeautifulSoup

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"
    }
# URL SEMILLA
url = 'https://stackoverflow.com/questions'
# REQUERIMIENTO AL SERVIDOR
respuesta = requests.get(url, headers = headers)
# INICIALIZAR BEAUTIFUL SOUP
soup = BeautifulSoup(respuesta.text)

div_preguntas = soup.find(id = 'questions')

preguntas = div_preguntas.find_all('div',class_= 'question-summary')

for pregunta in preguntas:
    print('Titulo: ', pregunta.find('h3').text)
    print(pregunta.find(class_='excerpt').text.replace('\n',' ').replace('\r',' ').strip())
