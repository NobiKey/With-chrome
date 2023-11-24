import scrapy
import re
from time import sleep
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapySeleniumPruebaFiSpider(scrapy.Spider):
    name = "scrapy-selenium-TT"

    def start_requests(self):
        url = 'https://www.tomaticket.es/'
        print("INICIO")
        print("")
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        driver = response.request.meta["driver"]
        print("En FI")
        print("")
        sleep(3)

        try:
            selec_lugar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//select[@id="IdLugar"]'))
            )
            lugar = Select(selec_lugar)
            lugar.select_by_visible_text('Gran Canaria')

            selec_categ = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//select[@id="IdTag"]'))
            )
            categ = Select(selec_categ)
            categ.select_by_visible_text('Música')

            try:
                disclaimer = driver.find_element(By.XPATH, '//p[text()="Consentir"]')
                disclaimer.click()
            except Exception as e:
                print(e)
                None

            boton = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="btn-filtro"]'))
            )
            boton.click()

        except Exception as e:
            print("ERROR")
            print(e)

        links_eventos = driver.find_elements(By.XPATH,
                                             '//div[@id="list-search-event"]/a[@class="eventtt destacados_TM"]')
        lista_links_eventos = []

        for link in links_eventos:
            lista_links_eventos.append(link.get_attribute("href"))

        i = 1
        for link in lista_links_eventos:
            sleep(2)

            if link != "javascript:;":
                driver.get(link)

                titulo = driver.find_element(By.XPATH, '//h1').text
                # print(titulo)

                resumen = driver.find_element(By.ID, 'TabContent1').text

                lugar = driver.find_element(By.XPATH, '//p[@class="nombre-recinto"]').text
                # print(lugar)

                try:
                    fecha = driver.find_element(By.XPATH, '//p[@class="fecha-info"]').text
                    # print(fecha)
                except:
                    fecha = "SIN FECHA DISPONIBLE"

                try:
                    link_compra = driver.find_element(By.XPATH, '//div[@class="titulopaso"]')
                    link_compra = link
                except:
                    try:
                        link_compra = driver.find_element(By.XPATH, '//a[@id="BotonExterno"]')
                        link_compra = link_compra.get_attribute("href")
                        # print(link_compra)
                    except:
                        link_compra = "NO HAY ENTRADAS DISPONIBLES"
                # print()

                yield {
                    "titulo": titulo,
                    "descripcion": resumen,
                    "fecha": fecha,
                    "lugar": lugar,
                    "link de compra": link_compra
                }

            sleep(2)
            driver.refresh()
            sleep(2)
            driver.back()
        else:
            abrir_info_evento = str(
                driver.find_element(By.XPATH, '//a[@href="javascript:;"][' + str(i) + ']').get_attribute(
                    "data-src")).replace('#', '')
            titulo = driver.find_element(By.XPATH, '//div[@id="' + abrir_info_evento + '"]//h4').get_attribute(
                "innerText")
            # print(titulo)
            fecha = driver.find_element(By.XPATH,
                                        '//div[@id="' + abrir_info_evento + '"]//p[@class="ticketera-parrafo"]').get_attribute(
                "innerText")
            # print(fecha)
            links_compra = driver.find_elements(By.XPATH, '//div[@id="' + abrir_info_evento + '"]//a')
            lista_links_compra = []
            for link in links_compra:
                link = link.get_attribute("href")
                # print(link)
                lista_links_compra.append(link)
            # print()

            yield {
                "titulo": titulo,
                "fecha": fecha,
                "link de compra": lista_links_compra
            }

            i += 1

        driver.close()

def limp_fech_hora(fecha):
    if (not "/" in fecha) and (not "-" in fecha):
        fecha = "SIN FECHA DISPONIBLE"
        hora = "SIN HORA DISPONIBLE"

    else:
        f_num = re.search(r"\d", fecha)
        f_num = f_num.start()
        fecha = fecha[f_num:]
        fecha = fecha.split()
        if ':' in fecha[-1]:
            hora = fecha[-1]
            if len(fecha) > 4:
                fecha = fecha[1]
            else:
                fecha = fecha[0]
        else:
            hora = "SIN HORA DISPONIBLE"
        if len(fecha) == 1:
            fecha = fecha[0]
            if fecha[-1] == ')':
                fecha = fecha[:-1]
        elif len(fecha) == 2:
            fecha = fecha[-1]
        elif len(fecha) == 3:
            separador = ''
            fecha = separador.join(fecha)
            fecha = fecha[:-1]

    return [fecha, hora]

def selec_eventos(driver, isla, tipo_event):
    selec_lugar = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="IdLugar"]'))
    )
    lugar = Select(selec_lugar)
    lugar.select_by_visible_text(isla)

    selec_categ = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//select[@id="IdTag"]'))
    )
    categ = Select(selec_categ)
    categ.select_by_visible_text(tipo_event)

    try:
        disclaimer = driver.find_element(By.XPATH, '//p[text()="Consentir"]')
        disclaimer.click()
    except Exception as e:
        print(e)
        None

    boton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="btn-filtro"]'))
    )
    boton.click()

def check_more_events(driver, link_compra):
    try:
        otros_eventos_enlaces = driver.find_elements(By.XPATH, '//div[@class="aviso-correo-evento"]/div/p/a')
        otros_eventos = driver.find_elements(By.XPATH, '//div[@class="aviso-correo-evento"]/div/p/a/strong')
        i = 0
        for texto in otros_eventos:
            exist_event = re.search(r"\d", texto.text)
            if exist_event and (int(texto.text) > 0):
                link_compra = link_compra + ". OTROS EVENTOS EN: " + otros_eventos_enlaces[i].get_attribute("href")
            i += 1
    except:
        None

    return link_compra