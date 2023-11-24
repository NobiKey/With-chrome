from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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