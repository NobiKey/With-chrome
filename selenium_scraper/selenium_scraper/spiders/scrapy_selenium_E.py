import scrapy
from time import sleep
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from datos_entrees import selec_eventos, limp_precios, limp_fech_hora, limp_titulo

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
