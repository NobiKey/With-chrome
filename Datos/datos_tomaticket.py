import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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