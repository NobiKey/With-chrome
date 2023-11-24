import scrapy
from time import sleep
from scrapy.crawler import CrawlerProcess
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class ScrapySeleniumPruebaFiSpider(scrapy.Spider):
    name = "scrapy-selenium-E"

    def start_requests(self):
        url = 'https://entrees.es/'
        print("INICIO")
        print("")
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        driver = response.request.meta["driver"]
        print("En FI")
        print("")
        sleep(3)

        try:
            selec_eventos(driver, "Gran Canaria")

        except Exception as e:
            print("ERROR")
            print(e)

        links_eventos = driver.find_elements(By.XPATH, '//div[@class="col-lg-12 col-xs-12 text-center event-content-grid-container "]/a')
        lista_links_eventos = []

        for link in links_eventos:
            lista_links_eventos.append(link.get_attribute("href"))

        for link in lista_links_eventos:
            sleep(2)

            driver.get(link)
            try:
                existen_datos = driver.find_element(By.XPATH, '//div[@class="col-lg-12 col-xs-12 event-details"]')

                titulo = driver.find_element(By.XPATH, '//h1[@class="event-details-name no-margin"]').text
                titulo = limp_titulo(titulo)
                print(titulo)

                fechas_y_hora = driver.find_element(By.XPATH, '//div[@class="date m-b-10"]').text
                try:
                    fecha, hora = limp_fech_hora(fechas_y_hora)
                except:
                    fecha = limp_fech_hora(fechas_y_hora)
                    hora = "HORAS EN ENLACE DE COMPRA"
                print(fecha)
                print(hora)

                recinto = driver.find_element(By.XPATH, '//span[text()="Recinto:"]/following-sibling::a').text
                print(recinto)

                duracion = driver.find_element(By.XPATH, '//div[text()="Duración"]/following-sibling::div').text
                print(duracion)

                try:
                    desde = driver.find_element(By.XPATH, '//div[@class="from"]').text
                    precio = desde + ' ' + driver.find_element(By.XPATH, '//div[@class="price float-right"]').text
                    precio = limp_precios(precio)
                except:
                    precio = driver.find_element(By.XPATH, '//div[@class="price-text"]').text
                print(precio)

                link_compra = driver.find_element(By.XPATH, '//a[@class="btn  btn-warning  btn-lg t-t-up col-lg-12 col-md-12 col-sm-12 col-xs-12"]')
                link_compra = link_compra.get_attribute("href")
                print(link_compra)

                descripcion = driver.find_element(By.XPATH, '//div[@id="sypnosis-content"]').text
                print(descripcion)

                url_img = driver.find_element(By.XPATH, '//img[@data-description]')
                url_img = url_img.get_attribute("src")
                print(url_img)
                print()

                yield {
                    "titulo": titulo,
                    "fecha": fecha,
                    "recinto": recinto,
                    "hora": hora,
                    "duración": duracion,
                    "precio": precio,
                    "descripción": descripcion,
                    "link_compra": link_compra,
                    "imagen url": url_img
                }

                sleep(2)
                driver.refresh()

            except:
                print("EL EVENTO NO TIENE LOS DATOS")
                print()

        driver.close()

def selec_eventos(driver, isla):
    try:
        disclaimer = driver.find_element(By.XPATH, '//a[@id="accept_cookie"]')
        disclaimer.click()
    except Exception as e:
        print(e)
        None

    selec_lugar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//select[@class="form-control category-select h-45 search-select"]'))
    )
    lugar = Select(selec_lugar)
    lugar.select_by_visible_text(isla)

def limp_titulo(titulo):
    titulo = titulo.replace('Entrada ', '')

    return titulo

def limp_precios(precios):
    if ' ' in precios[0]:
        precios = precios[1:]

    return precios

def limp_fech_hora(fechas_y_hora):
    if ':' in fechas_y_hora:
        index = fechas_y_hora.index(":")

        hora = fechas_y_hora[index-2:index+3]
        fecha = fechas_y_hora[:index-3]

        return [fecha, hora]

    else:
        return fechas_y_hora