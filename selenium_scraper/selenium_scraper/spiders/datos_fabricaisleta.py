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