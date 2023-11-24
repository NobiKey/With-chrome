import scrapy
from time import sleep
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By

class ScrapySeleniumPruebaFiSpider(scrapy.Spider):
    name = "scrapy-selenium-FI"
    #allowed_domains = ["www.fabricaisleta.com"]
    #start_urls = ["https://www.fabricaisleta.com/eventos/"]

    def start_requests(self):
        url = 'https://www.fabricaisleta.com/eventos/'
        print("INICIO")
        print("")
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        driver = response.request.meta["driver"]
        print("En FI")
        print("")
        sleep(3)

        while True:
            links_eventos = driver.find_elements(By.XPATH, '//div[@class="event_info"]/a')
            lista_links_eventos = []

            for link in links_eventos:
                lista_links_eventos.append(link.get_attribute("href"))

            for link in lista_links_eventos:
                sleep(2)
                driver.get(link)

                titulo = driver.find_element(By.XPATH, '//h1').text
                print(titulo)
                print("")

                img_url = driver.find_element(By.XPATH, '//img[@class="zoomImg"]')
                img_url = img_url.get_attribute("src")

                resumen = driver.find_element(By.XPATH, '//div[@id="tab-description"]/p').text

                try:
                    fecha = driver.find_element(By.XPATH, '//div[@class="summary entry-summary"]/p[not(contains(@style, "color")) and not(contains(@class, "price"))]/strong[not(contains(text(), "Lugar")) and not(contains(text(), "Hora"))]').text
                except:
                    fecha = "NO HAY FECHA DISPONIBLE"

                try:
                    lugar = driver.find_element(By.XPATH, '//div[@class="summary entry-summary"]/p[not(contains(@style, "color")) and not(contains(@class, "price"))]/strong[(contains(text(), "Lugar"))]').text
                    Lugar = limp_lugar(lugar)
                except:
                    Lugar = "NO HAY LUGAR DISPONIBLE"

                try:
                    hora = driver.find_element(By.XPATH, '//div[@class="summary entry-summary"]/p[not(contains(@style, "color")) and not(contains(@class, "price"))]/strong[(contains(text(), "Hora"))]').text
                    Hora = limp_hora(hora)
                except:
                    Hora = "NO HAY HORA DISPONIBLE"

                precios = driver.find_element(By.XPATH, '//div[@class="summary entry-summary"]/p[not(contains(@style, "color")) and (contains(@class, "price"))]').text
                if precios == '':
                    Precios = "PRECIOS NO DISPONIBLES"
                else:
                    Precios = limp_precios(precios)

                try:
                    enlace_compra = driver.find_element(By.XPATH, '//button[@class="single_add_to_cart_button button alt"]')
                    enlace_compra = link
                except:
                    enlace_compra = "ENTRADAS NO DISPONIBLES PARA COMPRAR EN WEB"

                driver.back()

                yield {
                    "titulo": titulo,
                    "imagen": img_url,
                    "descripcion": resumen,
                    "fecha": fecha,
                    "lugar": Lugar,
                    "hora": Hora,
                    "precios en puerta y web": Precios,
                    "link de compra": enlace_compra
                }

            try:
                paginar = driver.find_element(By.XPATH, '//p[text()="Siguiente"]')
                paginar.click()
            except:
                break

        driver.close()

def limp_lugar(lugar):
    lugar = lugar.split()
    Lugar = str()
    for i in lugar[1:]:
        Lugar += (i + ' ')
    Lugar = Lugar[:-1]

    return Lugar

def limp_hora(hora):
    hora = hora.split()
    Hora = hora[-1]

    return Hora

def limp_precios(precios):
    precios = precios.split("\n")
    Precios = str()
    for i in precios:
        Precios += (i + ', ')
    Precios = Precios[:-2]

    return Precios