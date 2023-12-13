import streamlit as st
import pandas as pd
import numpy as np
from math import pi

#st.title('Cálculo de gálibos')

st.set_page_config(
    page_title = 'Calculadora de gálibos',
    page_icon = '🚊',
    layout = 'centered'
)

st.markdown("# Cálculo de gálibos")
#st.sidebar.markdown("# Cálculo de gálibos")

st.write('La presente página sirve como recurso para el cálculo de los gálibos ferroviarios según la *Orden FOM/1630/2015, de 14 de julio, por el que se aprueba la "Instrucción Ferroviaria de Gálibos"*. Se deberán indicar las siguientes características correspondientes al trazado ferroviario del tramo de estudio, así como qué contorno de referencia se quiere emplear para el cálculo. Finalmente, se proporcionará el gálibo límite y nominal de implantación de osbtáculos. En la barra lateral es posible el cálculo del gálibo del pantógrafo, distancia entre vías, distancia con el borde de andén y la opción de generar un informe con todos los cálculos explicados.')

#st.session_state

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    ancho_via = st.selectbox("Ancho de vía:", ["Ibérico (1.668)", "Europeo (1.435)", "Métrico (1.000)"], help = "Para líneas con ancho mixto se debe realizar el cálculo por cada ancho de vía por separado.")
    tipo_linea = st.selectbox("Tipo de línea:", ["Nueva", "Acondicionada"])
    autopista_ferroviaria = st.selectbox("¿La línea es usada como autopista ferroviaria?", ["Sí", "No"])
    OBS = st.selectbox("¿Obstáculos se mueven solidariamente con la vía?", ["Sí", "No"])

with col2:
    tipo_via = st.selectbox("Tipo de vía:", ["Vía en balasto", "Vía en placa"])
    estado_via = st.selectbox("Estado de la vía:", ["Bueno", "Malo"])
    electrificacion_via = st.selectbox("¿La vía está electrificada?", ["Sí", "No"])

with col3:
    st.session_state.d = st.number_input("Peralte máximo de la vía (m):",format='%.3f')
    st.session_state.i = st.number_input("Insuficiencia de peralte máximo de la vía (m):",format='%.3f')
    st.session_state.r = st.number_input("Radio mínimo en planta (m):", format='%3.d')

with col4:
    st.session_state.RV = st.number_input("Radio mínimo de acuerdo vertical (m):",format='%3.d')
    st.session_state.v = st.number_input("Velocidad máxima de circulación (km/h):", format='%3.d', help = "En caso de no conocerse, se calculará la velocidad máxima posible para el peralte determinado.")

#ancho_via = st.selectbox("Ancho de vía:", ["Ibérico (1.668)", "Europeo (1.435)", "Métrico (1.000)"], help = "Para líneas con ancho mixto se debe realizar el cálculo por cada ancho de vía por separado.")
#tipo_linea = st.selectbox("Tipo de línea:", ["Nueva", "Acondicionada"])
#autopista_ferroviaria = st.selectbox("¿La línea es usada como autopista ferroviaria?", ["Sí", "No"])
#tipo_via = st.selectbox("Tipo de vía:", ["Vía en balasto", "Vía en placa"])
#estado_via = st.selectbox("Estado de la vía:", ["Bueno", "Malo"])
#electrificacion_via = st.selectbox("¿La vía está electrificada?", ["Sí", "No"])
#OBS = st.selectbox("¿Obstáculos se mueven solidariamente con la vía?", ["Sí", "No"])

if ancho_via == "Ibérico (1.668)":
    st.session_state.ancho_via = 1.668
    st.session_state.L = 1.733
elif ancho_via == "Europeo (1.435)":
    st.session_state.ancho_via = 1.435
    st.session_state.L = 1.5
elif ancho_via == "Métrico (1.000)":
    st.session_state.ancho_via = 1.000
    st.session_state.L = 1.055

if tipo_linea == "Nueva":
    tipo_linea = "nueva"
    st.session_state.tipo_linea = "nueva"
elif tipo_linea == "Acondicionada":
    tipo_linea = "acondicionada"
    st.session_state.tipo_linea = "acondicionada"

if autopista_ferroviaria == "Sí":
    autopista_ferroviaria = True
elif autopista_ferroviaria == "No":
    autopista_ferroviaria = False

if tipo_via == "Vía en balasto":
    st.session_state.tipo_via = "balasto"
elif tipo_via == "Vía en placa":
    st.session_state.tipo_via = "placa"

if estado_via == "Bueno":
    st.session_state.estado_via = "bueno"
elif estado_via == "Malo":
    st.session_state.estado_via = "malo"

if electrificacion_via == "Sí":
    electrificacion_via = "si"
elif electrificacion_via == "No":
    electrificacion_via = "no"

if OBS == "Sí":
    OBS = True
elif OBS == "No":
    OBS = False


print("El ancho de vía seleccionado es de %s metros." % (st.session_state.ancho_via))

#st.session_state.d = st.number_input("Peralte máximo de la vía (m):",format='%.3f')
#st.session_state.i = st.number_input("Insuficiencia de peralte máximo de la vía (m):",format='%.3f')
#st.session_state.r = st.number_input("Radio mínimo en planta (m):", format='%3.d')
#st.session_state.RV = st.number_input("Radio mínimo de acuerdo vertical (m):",format='%3.d')
#st.session_state.v = st.number_input("Velocidad máxima de circulación (km/h):", format='%3.d', help = "En caso de no conocerse, se calculará la velocidad máxima posible para el peralte determinado.")

if st.session_state.v == 0:
    st.session_state.v = ((st.session_state.i+st.session_state.d)*9.81*st.session_state.r/st.session_state.L)**0.5
else:
    st.session_state.v = st.session_state.v * 1000 / 3600

#st.write('La velocidad máxima de circulación es de %s m/s.' % (st.session_state.v),format='%3.f')

#st.write('El peralte de la vía es de %s metros.' % (st.session_state.d))

#Gálibo recomendado
##Partes altas
if tipo_linea == 'nueva':
    if st.session_state.ancho_via == 1.435:
        partes_altas_guia = 'GC'
    elif st.session_state.ancho_via == 1.668:
        partes_altas_guia = 'GEC16'
    elif st.session_state.ancho_via == '1.435+1.668':
        partes_altas_guia = 'GEC16+GC'
    elif st.session_state.ancho_via == 1.000 or st.session_state.ancho_via == 'metrica':
        if electrificacion_via == 'si':
            partes_altas_guia = 'GEE10'
        else:
            partes_altas = 'GED10'
    else:
        print("Has introducido un ancho de vía inexistente.")
elif tipo_linea == 'acondicionada':
    if st.session_state.ancho_via == 1.435:
        partes_altas_guia = 'GC (GB)'
    elif st.session_state.ancho_via == 1.668:
        partes_altas_guia = 'GEC16 (GEB16)'
    elif st.session_state.ancho_via == '1435+1668':
        partes_altas_guia = 'GEC16 + GC (GEC16+GB / GEB16+GC / GEB16+GB)'
    elif st.session_state.ancho_via == 1.000 or st.session_state.ancho_via == 'metrica':
        if electrificacion_via == 'si':
            partes_altas_guia = 'GEE10'
        else:
            partes_altas_guia = 'GED10'
    else:
        print("Has introducido un ancho de vía inexistente.")
##Partes bajas
if autopista_ferroviaria:
    if st.session_state.ancho_via == 1.435:
        partes_bajas_guia = 'GI3'
    elif st.session_state.ancho_via == 1.668:
        partes_bajas_guia = 'GEI3'
    elif st.session_state.ancho_via == 1.000 or st.session_state.ancho_via == 'metrico':
        if electrificacion_via == 'si':
            partes_bajas_guia = 'GEE10'
        else:
            partes_bajas_guia = 'GED10'
    else:
        print("Has introducido un ancho de vía inexistente.")
else:
    if st.session_state.ancho_via == 1.435:
        partes_bajas_guia = 'GI2'
    elif st.session_state.ancho_via == 1.668:
        partes_bajas_guia = 'GEI2'
    elif st.session_state.ancho_via == 1.000 or st.session_state.ancho_via == 'metrico':
        if electrificacion_via == 'si':
            partes_bajas_guia = 'GEE10'
        else:
            partes_bajas_guia = 'GED10'
    else:
        print("Has introducido un ancho de vía inexistente.")

if st.button("Gálibo recomendado"):
    st.write("El gálibo recomendado para las partes altas es el **%s** y para las partes bajas es el **%s**" % (partes_altas_guia, partes_bajas_guia))

#Selección contorno de referencia
if st.session_state.ancho_via == 1.435:
    st.session_state.partes_altas = st.selectbox("Contorno de referencia gálibo partes altas:", ["GA", "GB", "GC", "GEC14", "GC14"])
elif st.session_state.ancho_via == 1.668:
    st.session_state.partes_altas = st.selectbox("Contorno de referencia gálibo partes altas:", ["GEA16", "GEB16", "GEC16", "GHE16"])
elif st.session_state.ancho_via == 1.000:
    st.session_state.partes_altas = st.selectbox("Contorno de referencia gálibo partes altas:", ["GED10", "GEE10"])

if st.session_state.ancho_via == 1.435:
    st.session_state.partes_bajas = st.selectbox("Contorno de referencia gálibo partes bajas:", ["GI1", "GI2", "GI3"])
elif st.session_state.ancho_via == 1.668:
    st.session_state.partes_bajas = st.selectbox("Contorno de referencia gálibo partes bajas:", ["GEI1", "GEI2", "GEI3"])
elif st.session_state.ancho_via == 1.000:
    st.session_state.partes_bajas = st.selectbox("Contorno de referencia gálibo partes bajas:", ["GED10", "GEE10"])

#st.write('El gálibo seleccionado para las partes altas es %s' % (st.session_state.partes_altas))
#st.write('El gálibo seleccionado para las partes bajas es %s' % (st.session_state.partes_bajas))

#CONTORNOS DE REFERENCIA

#GEC16
def GEC16():
    p0 = [1.540, 4.700]
    p1 = [1.720, 3.320]
    p2 = [1.720, 1.150]
    p3 = [1.695, 1.150]
    p4 = [1.695, 0.400]
    puntos = [p0, p1, p2, p3, p4]
    bPT = 1.540
    hPT_max = 3.320
    hPT_min = 1.150
    bCR = 1.720
    hminCR = 0.400
    hPT = 4.700
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GHE16
def GHE16():
    p0 = [0.800, 4.330]
    p1 = [1.250, 4.100]
    p2 = [1.580, 3.700]
    p3 = [1.720, 3.320]
    p4 = [1.720, 1.150]
    p5 = [1.695, 1.150]
    p6 = [1.695, 0.600]
    p7 = [1.675, 0.600]
    p8 = [1.675, 0.400]
    puntos = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
    bPT = 0.800
    hPT_max = 3.320
    hPT_min = 1.150
    bCR = 1.720
    hminCR = 0.400
    hPT = 4.330
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GEA16
def GEA16():
    p0 = [0.761, 4.350]
    p1 = [1.250, 4.100]
    p2 = [1.580, 3.700]
    p3 = [1.720, 3.320]
    p4 = [1.720, 1.150]
    p5 = [1.695, 1.150]
    p6 = [1.695, 0.400]
    puntos = [p0, p1, p2, p3, p4, p5, p6]
    bPT = 0.761
    hPT_max = 3.320
    hPT_min = 1.150
    bCR = 1.720
    hminCR = 0.400
    hPT = 4.350
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GEB16
def GEB16():
    p0 = [0.761, 4.350]
    p1 = [1.360, 4.110]
    p2 = [1.580, 3.700]
    p3 = [1.720, 3.320]
    p4 = [1.720, 1.150]
    p5 = [1.695, 1.150]
    p6 = [1.695, 0.400]
    puntos = [p0, p1, p2, p3, p4, p5, p6]
    bPT = 0.761
    hPT_max = 3.320
    hPT_min = 1.150
    bCR = 1.720
    hminCR = 0.400
    hPT = 4.350
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GEI1
def GEI1():
    p0 = [1.637, 0.400]
    p1 = [1.367, 0.130]
    p2 = [1.292, 0.115]
    p3 = [0.964, 0.115]
    p4 = [0.964, 0.000]
    p5 = [0.834, 0.000]
    p6 = [0.834, -0.0036]
    p7 = [0.776, -0.0036]
    p8 = [0.776, 0.125]
    puntos = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
    return puntos

#GEI2
def GEI2():
    p0 = [1.637, 0.400]
    p1 = [1.367, 0.130]
    p2 = [1.292, 0.100]
    p3 = [1.052, 0.080]
    p4 = [0.964, 0.080]
    p5 = [0.964, 0.000]
    p6 = [0.834, 0.000]
    p7 = [0.834, -0.036]
    p8 = [0.776, -0.036]
    p9 = [0.776, 0.08]
    puntos = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
    return puntos

#GEI3
def GEI3():
    p0 = [1.637, 0.400]
    p1 = [1.450, 0.210]
    p2 = [1.425, 0.080]
    p3 = [0.964, 0.080]
    p4 = [0.964, 0.000]
    p5 = [0.834, 0.000]
    p6 = [0.834, -0.036]
    p7 = [0.776, -0.036]
    p8 = [0.776, 0.080]
    puntos = [p0, p1, p2, p3, p4, p5, p6, p7, p8]
    return puntos

#GA
def GA():
    p0 = [0.545, 4.350]
    p1 = [1.090, 4.080]
    p2 = [1.360, 3.880]
    p3 = [1.645, 3.250]
    p4 = [1.645, 1.170]
    p5 = [1.620, 1.170]
    p6 = [1.620, 0.400]
    puntos = [p0, p1, p2, p3, p4, p5, p6]
    bPT = 0.545
    hPT_max = 3.250
    hPT_min = 1.170
    bCR = 1.645
    hminCR = 0.400
    hPT = 4.350
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GB
def GB():
    p0 = [0.545, 4.350]
    p1 = [1.360, 4.110]
    p2 = [1.645, 3.250]
    p3 = [1.645, 1.170]
    p4 = [1.620, 1.170]
    p5 = [1.620, 0.400]
    puntos = [p0, p1, p2, p3, p4, p5]
    bPT = 0.545
    hPT_max = 3.250
    hPT_min = 1.170
    bCR = 1.645
    hminCR = 0.400
    hPT = 4.350
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GC
def GC():
    p0 = [1.540, 4.700]
    p1 = [1.645, 3.550]
    p2 = [1.645, 1.170]
    p3 = [1.620, 1.170]
    p4 = [1.620, 0.400]
    puntos = [p0, p1, p2, p3, p4]
    bPT = 1.540
    hPT_max = 3.550
    hPT_min = 1.170
    bCR = 1.645
    hminCR = 0.400
    hPT = 4.700
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GI1
def GI1():
    p0 = [1.620, 0.400]
    p1 = [1.520, 0.400]
    p2 = [1.250, 0.130]
    p3 = [1.212, 0.115]
    p4 = [0.8475, 0.115]
    p5 = [0.8475, 0.000]
    p6 = [0.7175, 0.000]
    p7 = [0.7175, -0.036]
    p8 = [0.6595, -0.036]
    p9 = [0.6595, 0.115]
    puntos = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
    return puntos

#GI2
def GI2():
    p0 = [1.620, 0.400]
    p1 = [1.520, 0.400]
    p2 = [1.250, 0.130]
    p3 = [1.175, 0.100]
    p4 = [0.935, 0.080]
    p5 = [0.8475, 0.080]
    p6 = [0.8475, 0.000]
    p7 = [0.7175, 0.000]
    p8 = [0.7175, -0.036]
    p9 = [0.6595, -0.036]
    p10 = [0.6595, 0.080]
    puntos = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10]
    return puntos

#GI3
def GI3():
    p0 = [1.620, 0.400]
    p1 = [1.520, 0.400]
    p2 = [1.450, 0.250]
    p3 = [1.425, 0.080]
    p4 = [0.8475, 0.080]
    p5 = [0.8475, 0.000]
    p6 = [0.7175, 0.000]
    p7 = [0.7175, -0.036]
    p8 = [0.6595, -0.036]
    p9 = [0.6595, 0.080]
    puntos = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
    return puntos

#GEE10
def GEE10():
    p0 = [0.500, 4.100]
    p1 = [1.185, 3.900]
    p2 = [1.530, 3.550]
    p3 = [1.530, 0.400]
    puntos = [p0, p1, p2, p3]
    bPT = 0.500
    hPT_max = 3.900
    hPT_min = 3.550
    bCR = 1.530
    hminCR = 0.400
    hPT = 4.100
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GED10
def GED10():
    p0 = [0.750, 3.900]
    p1 = [1.150, 3.800]
    p2 = [1.530, 3.550]
    p3 = [1.530, 0.400]
    puntos = [p0, p1, p2, p3]
    bPT = 0.750
    hPT_max = 3.800
    hPT_min = 3.550
    bCR = 1.530
    hminCR = 0.400
    hPT = 3.900
    return puntos, bPT, hPT_max, hPT_min, bCR, hminCR, hPT

#GEE10 y GED10 partes bajas
def GEE10I():
    p0 = [1.440, 0.400]
    p1 = [1.440, 0.150]
    p2 = [0.870, 0.150]
    p3 = [0.870, 0.100]
    p4 = [0.630, 0.100]
    p5 = [0.630, 0.000]
    p6 = [0.500, 0.000]
    p7 = [0.500, -0.036]
    p8 = [0.442, -0.036]
    p9 = [0.442, 0.080]
    p10 = [0.150, 0.080]
    p11 = [0.150, 0.100]
    puntos = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11]
    return puntos

#CÁLCULO DE GÁLIBOS

#Generación contorno de estudio
##Partes altas
if st.session_state.partes_altas == 'GHE16':
    puntos_PA = GHE16()[0]
    bPT = GHE16()[1]
    st.session_state.hPT_max = GHE16()[2]
    hPT_min = GHE16()[3]
    st.session_state.bCR = GHE16()[4]
    st.session_state.hminCR = GHE16()[5]
    hPT = GHE16()[6]
elif st.session_state.partes_altas == 'GEA16':
    puntos_PA = GEA16()[0]
    bPT = GEA16()[1]
    st.session_state.hPT_max = GEA16()[2]
    hPT_min = GEA16()[3]
    st.session_state.bCR = GEA16()[4]
    st.session_state.hminCR = GEA16()[5]
    hPT = GEA16()[6]
elif st.session_state.partes_altas == 'GEB16':
    puntos_PA = GEB16()[0]
    bPT = GEB16()[1]
    st.session_state.hPT_max = GEB16()[2]
    hPT_min = GEB16()[3]
    st.session_state.bCR = GEB16()[4]
    st.session_state.hminCR = GEB16()[5]
    hPT = GEB16()[6]
elif st.session_state.partes_altas == 'GEC16':
    puntos_PA = GEC16()[0]
    bPT = GEC16()[1]
    st.session_state.hPT_max = GEC16()[2]
    hPT_min = GEC16()[3]
    st.session_state.bCR = GEC16()[4]
    st.session_state.hminCR = GEC16()[5]
    hPT = GEC16()[6]
elif st.session_state.partes_altas == 'GA':
    puntos_PA = GA()[0]
    bPT = GA()[1]
    st.session_state.hPT_max = GA()[2]
    hPT_min = GA()[3]
    st.session_state.bCR = GA()[4]
    st.session_state.hminCR = GA()[5]
    hPT = GA()[6]
elif st.session_state.partes_altas == 'GB':
    puntos_PA = GB()[0]
    bPT = GB()[1]
    st.session_state.hPT_max = GB()[2]
    hPT_min = GB()[3]
    st.session_state.bCR = GB()[4]
    st.session_state.hminCR = GB()[5]
    hPT = GB()[6]
elif st.session_state.partes_altas == 'GC':
    puntos_PA = GC()[0]
    bPT = GC()[1]
    st.session_state.hPT_max = GC()[2]
    hPT_min = GC()[3]
    st.session_state.bCR = GC()[4]
    st.session_state.hminCR = GC()[5]
    hPT = GC()[6]
elif st.session_state.partes_altas == 'GEE10':
    puntos_PA = GEE10()[0]
    bPT = GEE10()[1]
    st.session_state.hPT_max = GEE10()[2]
    hPT_min = GEE10()[3]
    st.session_state.bCR = GEE10()[4]
    st.session_state.hminCR = GEE10()[5]
    hPT = GEE10()[6]
elif st.session_state.partes_altas == 'GED10':
    puntos_PA = GED10()[0]
    bPT = GED10()[1]
    st.session_state.hPT_max = GED10()[2]
    hPT_min = GED10()[3]
    st.session_state.bCR = GED10()[4]
    st.session_state.hminCR = GED10()[5]
    hPT = GED10()[6]
##Partes bajas
if st.session_state.partes_bajas == 'GEI1':
    puntos_PB = GEI1()
elif st.session_state.partes_bajas == 'GEI2':
    puntos_PB = GEI2()
elif st.session_state.partes_bajas == 'GEI3':
    puntos_PB = GEI3()
elif st.session_state.partes_bajas == 'GEE10' or st.session_state.partes_bajas == 'GED10':
    puntos_PB = GEE10I()
elif st.session_state.partes_bajas == 'GI1':
    puntos_PB = GI1()
elif st.session_state.partes_bajas == 'GI2':
    puntos_PB = GI2()
elif st.session_state.partes_bajas == 'GI3':
    partes_PB = GI3()
##Partes altas y partes bajas
puntos = puntos_PA + puntos_PB



#Definición funciones cálculos
def k(h):
    k = 0
    if h > 0.4:
        if st.session_state.partes_altas == 'GHE16' or st.session_state.partes_altas == 'GEC16' or st.session_state.partes_altas == 'GC':
            k = 0
        elif st.session_state.partes_altas == 'GEA16':
            if h <= 3.32:
                k = 0
            elif h < 3.7:
                k = (h - 3.32) / 0.38
            else:
                k = 1
        elif st.session_state.partes_altas == 'GEB16':
            if h <= 3.32:
                k = 0
            elif h < 4.11:
                k = (h - 3.32) / 0.79
            else:
                k = 1
        elif st.session_state.partes_altas == 'GA':
            if h <= 3.25:
                k = 0
            elif h < 3.88:
                k = (h - 3.25) / 0.63
            else:
                k = 1
        elif st.session_state.partes_altas == 'GB':
            if h <= 3.25:
                k = 0
            elif h < 4.11:
                k = (h - 3.25) / 0.86
            else:
                k = 1
    else:
        if st.session_state.partes_bajas == 'GEI1' or st.session_state.partes_bajas == 'GEI2':
            k = 0
        elif st.session_state.partes_bajas == 'GEI3':
            if h > 0.25:
                k = (0.4 - h) / 0.15
            else:
                k = 1
        elif st.session_state.partes_bajas == 'GI1' or st.session_state.partes_bajas == 'GI2':
            k = 0
        elif st.session_state.partes_bajas == 'GI3':
            if h > 0.25:
                k = (0.4 - h) / 0.15
            else:
                k = 1
    return k

def s0(h):
    s0 = 0
    if h > 0.4:
        if st.session_state.partes_altas == 'GHE16' or st.session_state.partes_altas == 'GEC16' or st.session_state.partes_altas == 'GC' or st.session_state.partes_altas == 'GEE10' or st.session_state.partes_altas == 'GED10':
            s0 = 0.4
        elif st.session_state.partes_altas == 'GEA16':
            if h <= 3.32:
                s0 = 0.4
            elif h < 3.7:
                s0 = (4.84 - h) / 3.8
            else:
                s0 = 0.3
        elif st.session_state.partes_altas == 'GEB16':
            if h <= 3.32:
                s0 = 0.4
            elif h < 4.11:
                s0 = (6.48 - h) / 7.9
            else:
                s0 = 0.3
        elif st.session_state.partes_altas == 'GA':
            if h <= 3.25:
                s0 = 0.4
            elif h < 3.88:
                s0 = (5.77 - h) / 6.3
            else:
                s0 = 0.4
        elif st.session_state.partes_altas == 'GB':
            if h <= 3.25:
                s0 = 0.4
            elif h < 4.11:
                s0 = (6.69 - h) / 8.6
            else:
                s0 = 0.3
        else:
            s0 = 0.4
    return s0

#Salientes
def Si_a(h,R):
    Si = 0
    Sa = 0
    if h > 0.4:
        if st.session_state.partes_altas == 'GEE10' or st.session_state.partes_altas == 'GED10':
            if R >= 100:
                Si = 1.5 / R + 0.015
                Sa = Si
            else:
                Si = 20 / R - 0.185 + 0.015
                Sa = 24 / R - 0.225 + 0.015
        else:
            if R >= 250:
                if st.session_state.partes_altas == 'GHE16' or st.session_state.partes_altas == 'GEC16' or st.session_state.partes_altas == 'GC':
                    Si = 3.75 / R + 0.015
                    Sa = Si
                elif st.session_state.partes_altas == 'GEA16' or st.session_state.partes_altas == 'GEB16':
                    if h <= 3.32:
                        Si = 3.75 / R + 0.015
                        Sa = Si
                    elif h > 3.32:
                        Si = 3.75 / R + 16.25 * k(h) / R + 0.015
                        Sa = Si
                elif st.session_state.partes_altas == 'GA' or st.session_state.partes_altas == 'GB':
                    if h <= 3.25:
                        Si = 3.75 / R + 0.015
                        Sa = Si
                    elif h > 3.25:
                        Si = 3.75 / R + 16.25 * k(h) / R + 0.015
                        Sa = Si
            elif R >= 150:
                if st.session_state.partes_altas == 'GHE16' or st.session_state.partes_altas == 'GEC16' or st.session_state.partes_altas == 'GC':
                    Si = 50 / R - 0.185 + 0.015
                    Sa = 60 / R - 0.225 + 0.015
                elif st.session_state.partes_altas == 'GEA16' or st.session_state.partes_altas == 'GEB16':
                    if h <= 3.32:
                        Si = 50 / R - 0.185 + 0.015
                        Sa = 60 / R - 0.225 + 0.015
                    elif h > 3.32:
                        Si = 50 / R - 0.185 + 0.065 * k(h) + 0.015
                        Sa = 60 / R - 0.225 + k(h) * (0.105 - 10 / R) + 0.015
                elif st.session_state.partes_altas == 'GA' or st.session_state.partes_altas == 'GB':
                    if h <= 3.25:
                        Si = 50 / R - 0.185 + 0.015
                        Sa = 60 / R - 0.225 + 0.015
                    elif h > 3.25:
                        Si = 50 / R - 0.185 + 0.065 * k(h) + 0.015
                        Sa = 60 / R - 0.225 + k(h) * (0.105 - 10 / R) + 0.015
            else:
                Si = 0
                Sa = 0
    elif h <= 0.4:
        if st.session_state.partes_bajas == 'GEE10' or st.session_state.partes_bajas == 'GED10':
            if R >= 100:
                Si = 1 / R + 0.015
                Sa = Si
            else:
                Si = 20 / R - 0.19 + 0.015
                Sa = 24 / R - 0.23 + 0.015
        else:
            if R >= 250:
                if st.session_state.partes_bajas == 'GEI1' or st.session_state.partes_bajas == 'GEI2':
                    Si = 2.5 / R + 0.015
                    Sa = Si
                elif st.session_state.partes_bajas == 'GEI3':
                    Si = 2.5 / R + 0.015
                    Sa = 2.5 / R - 2.5 * k(h) / R + 0.015
                elif st.session_state.partes_bajas == 'GI1' or st.session_state.partes_bajas == 'GI2':
                    Si = 2.5 / R + 0.015
                    Sa = Si
                elif st.session_state.partes_bajas == 'GI3':
                    Si = 2.5 / R + 0.015
                    Sa = 2.5 / R - 2.5 * k(h) / R + 0.015
            elif R >= 150:
                if st.session_state.partes_bajas == 'GEI1' or st.session_state.partes_bajas == 'GEI2':
                    Si = 50 / R - 0.19 + 0.015
                    Sa = 60 / R - 0.23 + 0.015
                elif st.session_state.partes_bajas == 'GEI3':
                    Si = 50 / R - 0.19 + k * (0.05 - 12.5 / R) + 0.015
                    Sa = 60 / R - 0.23 + k * (0.07 - 20 / R) + 0.015
                elif st.session_state.partes_bajas == 'GI1' or st.session_state.partes_bajas == 'GI2':
                    Si = 50 / R - 0.19 + 0.015
                    Sa = 60 / R - 0.23 + 0.015
                elif st.session_state.partes_bajas == 'GI3':
                    Si = 50 / R - 0.19 + k(h) * (0.05 - 12.5 / R) + 0.015
                    Sa = 60 / R - 0.23 + k(h) * (0.07 - 20 / R) + 0.015
                else:
                    Si = 0
                    Sa = 0
    return Si,Sa

#Desplazamientos cuasiestáticos laterales
##Vehículo parado
def qSDi_a(h,D):
    qsDi = 0
    qsDa = 0
    if st.session_state.ancho_via == 1.000:
        D0 = 0.07
        hc0 = 0.5
        L = 1.055
    else:
        D0 = 0.05
        hc0 = 0.5
        if st.session_state.ancho_via == 1.435:
            L = 1.5
        elif st.session_state.ancho_via == 1.668:
            L = 1.733
    if D > D0 and h > hc0:
        qSDi = s0(h) / L * (D - D0) * (h - hc0)
        qSDa = qSDi
    else:
        qSDi = 0
        qSDa = 0
    return qSDi,qSDa

##Vehículo circulando a velocidad máxima
def qSIi_a(h,I):
    qSIi = 0
    qSIa = 0
    if st.session_state.ancho_via == 1.000:
        I0 = 0.07
        hc0 = 0.5
        L = 1.055
    elif st.session_state.ancho_via == 1.435:
        L = 1.5
        I0 = 0.05
        hc0 = 0.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
        I0 = 0.05
        hc0 = 0.5
    if I > I0 and h > hc0:
        qSIi = s0(h) / L * (I - I0) * (h - hc0)
        qSIa = qSIi
    else:
        qSIi = 0
        qSIa = 0
    return qSIi, qSIa

#Márgenes complementarios laterales y verticales
def M3b_h(h):
    M3b = 0
    M3h = 0
    if h < 0.4:
        M3b = 0
        M3h = 0
    else:
        M3b = 0.2
        M3h = 0.15
    return M3b, M3h

#Inscripción en acuerdos verticales
#Comprovar on es posa el signe
def hRv(h, Rv):
    hRv = 0
    if Rv >= 500:
        h_bmax = 'TBD'
        hRv = 50 / Rv
    else:
        hRv = 0
    return hRv

#Desplazamientos cuasiestáticos perpendiculares al plano de rodadura
##Vehículo parado
def hPTDi_a(h,D):
    hPTDi = 0
    hPTDa = 0
    if h == hPT:
        if st.session_state.ancho_via == 1.000:
            D0 = 0.07
            hc0 = 0.5
            L = 1.055
        else:
            D0 = 0.05
            hc0 = 0.5
        if st.session_state.ancho_via == 1.435:
                L = 1.5
        elif st.session_state.ancho_via == 1.668:
                L = 1.733
        if D > D0:
            hPTDi = bPT * s0(h) / L * (D - D0)
            hPTDa = hPTDi
    else:
        hPTDi = 0
        hPTDa = 0
    return hPTDi, hPTDa

##Vehículo circulando a velocidad máxima
#S'ha de definir bPT
def hPTIi_a(h,I):
    hPTIi = 0
    hPTIa = 0
    if h == hPT:
        if st.session_state.ancho_via == 1.000:
            I0 = 0.07
            hc0 = 0.5
            L = 1.055
        else:
            I0 = 0.05
            hc0 = 0.5
        if st.session_state.ancho_via == 1.435:
            L = 1.5
        elif st.session_state.ancho_via == 1.668:
            L = 1.733
        if I > I0:
            hPTIi = bPT * s0(h) / L * (I - I0)
            hPTIa = hPTIi
        else:
            hPTIi = 0
            hPTIa = 0
    else:
        hPTIi = 0
        hPTIa = 0
    return hPTIi, hPTIa

#Definición valores desplazamientos aleatorios
##Desplazamiento de vía
def Tvia():
    if st.session_state.tipo_via.lower() == 'balasto':
        Tvia = 0.025
    elif st.session_state.tipo_via.lower() == 'placa':
        Tvia = 0.005
    return Tvia

##Desviación de peralte
def TD(vmax):
    if st.session_state.tipo_via.lower() == 'balasto':
        if st.session_state.ancho_via == 1.000:
            TD = 0.02
        else:
            if vmax > 80:
                TD = 0.015
            else:
                TD = 0.02
    elif st.session_state.tipo_via.lower() == 'placa':
        if st.session_state.ancho_via == 1.000:
            TD = 0.003
        else:
            TD = 0.005
    return TD

##Disimetría debida al reparto de cargas
alpha_c = 0.77 * pi / 180

##Disimetría debida al reglaje de las suspensiones
alpha_susp = 0.23 * pi / 180

##Oscilaciones por irregularidades
def alpha_osc(h,x):
    alpha_osc = 0
    if st.session_state.tipo_via == 'balasto':
        if st.session_state.ancho_via == 1.000:
            if x.lower() == 'interior':
                alpha_osc = 0.2
            elif x.lower() == 'exterior':
                alpha_osc = 1
        else:
            if st.session_state.estado_via == 'bueno':
                if s0(h) == 0.4:
                    if x.lower() == 'interior':
                        alpha_osc = 0.1
                    elif x.lower() == 'exterior':
                        alpha_osc = 0.6
                elif s0(h) == 0.3:
                    if x.lower() == 'interior':
                        alpha_osc = 0.08
                    elif x.lower() == 'exterior':
                        alpha_osc = 0.45
            elif st.session_state.estado_via == 'malo':
                if s0(h) == 0.4:
                    if x.lower() == 'interior':
                        alpha_osc = 0.2
                    elif x.lower() == 'exterior':
                        alpha_osc = 1
                elif s0(h) == 0.3:
                    if x.lower() == 'interior':
                        alpha_osc = 0.15
                    elif x.lower() == 'exterior':
                        alpha_osc = 0.75
    elif st.session_state.tipo_via == 'placa':
        if x.lower() == 'interior':
            if s0(h) == 0.4:
                alpha_osc = 0.1
            elif s0(h) == 0.3:
                alpha_osc = 0.08
        elif x.lower() == 'exterior':
            if s0(h) == 0.4:
                alpha_osc = 0.6
            elif s0(h) == 0.3:
                alpha_osc = 0.45
    alpha_osc = alpha_osc * pi / 180
    return alpha_osc

##Desplazamiento vertical de la vía
def TN(h,obs):
    if h <= 0.4 and obs == True:
        TN = 0.005
    else:
        TN = 0.02
    return TN

##Factor de seguridad para la determinación del gálibo límite de implantación de obstáculos
#Controlar desplazamientos aleatorios laterales
def K(h):
    if h < 0.5:
        K = 1
    else:
        K = 1.2
    return K

##Factor de seguridad para la determinación del gálibo mecánico del pantógrafo
K_bis = 1

def j1(h,v,ext):
    hc0 =0.5
    if st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    if h > hc0:
        j1 = K(h)*(Tvia()**2+(h+s0(h)*(h-hc0))**2*(TD(v)/L)**2+(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc(h,ext)**2))*(h-hc0)**2)**0.5
    else:
        j1 = K(h)*(Tvia()**2+h**2*(TD(v)/L)**2)**0.5
    return j1

def j2(h,v):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    j2 = K(h)*(Tvia()**2+(h*TD(v)/L)**2)**0.5
    return j2

def j1_bis(h,v,ext):
    hc0 = 0.5
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    if h > hc0:
        aux = Tvia()**2-(h+s0(h)*(h-hc0))**2*(TD(v)/L)**2-(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc(h,ext)**2))*(h-hc0)**2
        if aux >= 0:
            j1_bis = K(h)*aux**0.5
        else:
            j1_bis = - K(h)*(-1*aux)**0.5
    else:
        aux = Tvia()**2-h**2*(TD(v)/L)**2
        if aux >= 0:
            j1_bis = K(h)*aux**0.5
        else:
            j1_bis = - K(h)*(-1*aux)**0.5
    return j1_bis

def j2_bis(h,v):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    j2_bis = K(h)*(Tvia()**2-(h*TD(v)/L)**2)**0.5
    return j2_bis

def Vi1(h,v,ext,obs):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    if (1 + s0(h)) * bPT < (L / 2):
        aux = TN(h,obs)**2+(-(1+s0(h))*bPT+L/2)**2*(TD(v)/L)**2-bPT**2*(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc(h,ext))**2)
        if aux >= 0:
            Vi1 = K(h)*(aux)**0.5
        else:
            Vi1 = - K(h)*(-aux)**0.5
    else:
        aux = TN(h,obs)**2-bPT**2*(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc(h,ext))**2)
        if aux >= 0:
            Vi1 = K(h) * (aux)**0.5
        else:
            Vi1 = - K(h) * (-aux)**0.5
    return Vi1

def Vi1_bis(h,v,ext, obs):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    if (1 + s0(h)) * bPT > (L / 2):
        aux = TN(h,obs)**2+((1+s0(h))*bPT-L/2)**2*(TD(v)/L)**2+bPT**2*(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc(h,ext))**2)
        if aux >= 0:
            Vi1_bis = K(h) * (aux)**0.5
        else:
            Vi1_bis = - K(h)* (-aux)**0.5
    else:
        aux = TN(h,obs)**2+bPT**2*(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc(h,ext))**2)
        if aux >= 0:
            Vi1_bis = K(h) * (aux)**0.5
        else:
            Vi1_bis = -K(h) * (-aux)**0.5
    return Vi1_bis

def Vi2(h,obs):
    Vi2 = TN(h,obs)
    return Vi2

def Va2(h,obs):
    Va2 = TN(h,obs)
    return Va2

def Va1(h,v,ext,obs):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    aux = TN(h,obs)**2-((1+s0(h))*bPT+L/2)**2*(TD(v)/L)**2-bPT**2*(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc(h,ext))**2)
    if aux >= 0:
        Va1 = K(h) * (aux)**0.5
    else:
        Va1 = - K(h) * (-aux)**0.5
    return Va1

def Va1_bis(h,v,ext,obs):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    aux = TN(h,obs)**2+((1+s0(h))*bPT+L/2)**2*(TD(v)/L)**2+bPT**2*(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc(h,ext))**2)
    if aux >= 0:
        Va1_bis = K(h) * (aux)**0.5
    else:
        Va1_bis = - K(h) * (-aux)**0.5
    return Va1_bis

def Vi2_bis(h,obs):
    Vi2_bis = TN(h,obs)
    return Vi2_bis

def Va2_bis(h,obs):
    Va2_bis = TN(h,obs)
    return Va2_bis

def j3(h,vmax,ext):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    hc0 = 0.5
    if h > hc0:
        j3 = Tvia()+(h+s0(h)*(h-hc0))*TD(vmax)/L+(h-hc0)*(np.tan(alpha_susp)+np.tan(alpha_c)+np.tan(alpha_osc(h,ext)))
    else:
        j3 = Tvia() + h * TD(vmax) / L
    return j3

def j4(h,vmax):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    j4 = Tvia() + h * TD(vmax) / L
    return j4

def j3_bis(h,vmax,ext):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    hc0 = 0.5
    if h > hc0:
        j3_bis = Tvia()-(h+s0(h)*(h-hc0))*TD(vmax)/L-(h-hc0)*(np.tan(alpha_susp)+np.tan(alpha_c)+np.tan(alpha_osc(h,ext)))
    else:
        j3_bis = Tvia() - h * TD(vmax) / L
    return j3_bis

def j4_bis(h,vmax):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    j4_bis = Tvia() - h * TD(vmax) / L
    return j4_bis

def Vi3(h,bPT,vmax,ext,obs):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    aux = L / 2 - (1 + s0(h)) * bPT
    if aux > 0:
        Vi3 = TN(h,obs) + aux * TD(vmax) / L - bPT * (np.tan(alpha_susp) + np.tan(alpha_c) + np.tan(alpha_osc(h,ext)))
    else:
        Vi3 = TN(h,obs) - bPT * (np.tan(alpha_susp) + np.tan(alpha_c) + np.tan(alpha_osc(h,ext)))
    return Vi3

def Va3(h,bPT,vmax,ext,obs):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    Va3 = TN(h,obs)-((1+s0(h))*bPT+L/2)*TD(vmax)/L-bPT*(np.tan(alpha_susp)+np.tan(alpha_c)+np.tan(alpha_osc(h,ext)))
    return Va3

def Vi4(h,obs):
    Vi4 = TN(h,obs)
    return Vi4

def Va4(h,obs):
    Va4 = TN(h,obs)
    return Va4

def Vi4_bis(h,obs):
    Vi4_bis = TN(h,obs)
    return Vi4_bis

def Va4_bis(h,obs):
    Va4_bis = TN(h,obs)
    return Va4_bis

def Vi3_bis(h,bPT,vmax,ext,obs):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    aux = (1 + s0(h)) * bPT - L / 2
    if aux > 0:
        Vi3_bis = TN(h,obs) + aux * TD(vmax) / L + bPT * (np.tan(alpha_susp) + np.tan(alpha_c) + np.tan(alpha_osc(h,ext)))
    else:
        Vi3_bis = TN(h,obs) + bPT * (np.tan(alpha_susp) + np.tan(alpha_c) + np.tan(alpha_osc(h,ext)))
    return Vi3_bis

def Va3_bis(h,bPT,vmax,ext,obs):
    if st.session_state.ancho_via == 1.435:
        L = 1.5
    elif st.session_state.ancho_via == 1.668:
        L = 1.733
    elif st.session_state.ancho_via == 1.000:
        L = 1.055
    Va3_bis = TN(h,obs)+((1+s0(h))*bPT+L/2)*TD(vmax)/L+bPT*(np.tan(alpha_susp)+np.tan(alpha_c)+np.tan(alpha_osc(h,ext)))
    return Va3_bis

#GÁLIBO LÍMITE DE IMPLANTACIÓN DE OBSTÁCULOS

##Punto PT
def PT(b,h):
    #Lado interior
    ## b max con h compatible
    ### v max
    bbvi = b +  Si_a(h,st.session_state.r)[0] - qSIi_a(h,st.session_state.i)[0] + j1(h,st.session_state.v,'interior')
    hbvi = h + hRv(h,st.session_state.RV) + hPTIi_a(h,st.session_state.i)[0] +Vi1(h,st.session_state.v,'exterior',OBS)
    PTbvi = [-bbvi,hbvi]
    ### v = 0
    bb0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j1(h,st.session_state.v,'interior')
    hb0i = h + hRv(h,st.session_state.RV) - hPTDi_a(h,st.session_state.d)[0] + Vi1(h,st.session_state.v,'exterior',OBS)
    PTb0i = [-bb0i,hb0i]
    ## h max con b compatible
    ### v max
    bhvi = b + Si_a(h,st.session_state.r)[0] - qSIi_a(h,st.session_state.i)[0] + j1_bis(h,st.session_state.v,'interior')
    hhvi = h + hRv(h,st.session_state.RV) + hPTIi_a(h,st.session_state.i)[0] + Vi1_bis(h,st.session_state.v,'exterior',OBS)
    PThvi = [-bhvi,hhvi]
    ### v = 0
    bh0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j1_bis(h,st.session_state.v,'interior')
    hh0i = h + hRv(h,st.session_state.RV) - hPTDi_a(h,st.session_state.d)[0] + Vi1_bis(h,st.session_state.v,'exterior',OBS)
    PTh0i = [-bh0i,hh0i]
    #Lado exterior
    ## b max con h compatible
    ### v max
    bbve = b +  Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j1(h,st.session_state.v,'exterior')
    hbve = h + hRv(h,st.session_state.RV) - hPTIi_a(h,st.session_state.i)[1] + Va1(h,st.session_state.v,'interior',OBS)
    PTbve = [bbve,hbve]
    ### v = 0
    bb0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j1(h,st.session_state.v,'exterior')
    hb0e = h + hRv(h,st.session_state.RV) + hPTDi_a(h,st.session_state.d)[1] + Va1(h,st.session_state.v,'interior',OBS)
    PTb0e = [bb0e,hb0e]
    ## h max con b compatible
    ### v max
    bhve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j1_bis(h,st.session_state.v,'exterior')
    hhve = h + hRv(h,st.session_state.RV) - hPTIi_a(h,st.session_state.i)[1] + Va1_bis(h,st.session_state.v,'interior',OBS)
    PThve = [bhve,hhve]
    ### v = 0
    bh0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j1_bis(h,st.session_state.v,'exterior')
    hh0e = h + hRv(h,st.session_state.RV) + hPTDi_a(h,st.session_state.d)[1] + Va1_bis(h,st.session_state.v,'interior',OBS)
    PTh0e = [bh0e,hh0e]
    #print(PTbvi,PTbve)
    #print(PTb0i,PTb0e)
    #print(PThvi,PThve)
    #print(PTh0i,PTh0e)
    return PTbvi,PTbve,PTb0i,PTb0e,PThvi,PThve,PTh0i,PTh0e

##Partes altas: puntos por encima de la anchura máxima
def PA_above(b,h):
    #Lado interior
    ## b max con h compatible
    ### v max
    bbvi = b + Si_a(h,st.session_state.r)[0]  - qSIi_a(h,st.session_state.i)[0] + j1(h,st.session_state.v,'interior')
    hbvi = h + hRv(h,st.session_state.RV) + Vi2(h,OBS)
    PAbvi = [-bbvi,hbvi]
    ### v = 0
    bb0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j1(h,st.session_state.v,'interior')
    hb0i = h + hRv(h,st.session_state.RV) + Vi2(h,OBS)
    PAb0i = [-bb0i,hb0i]
    ## h max con b compatible
    ### v max
    bhvi = b + Si_a(h,st.session_state.r)[0] - qSIi_a(h,st.session_state.i)[0] + j1_bis(h,st.session_state.v,'interior')
    hhvi = h + hRv(h,st.session_state.RV) + Vi2_bis(h,OBS)
    PAhvi = [-bhvi,hhvi]
    ### v = 0
    bh0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j1_bis(h,st.session_state.v,'interior')
    hh0i = h + hRv(h,st.session_state.RV) + Vi2_bis(h,OBS)
    PAh0i = [-bh0i,hh0i]
    #Lado exterior
    ## b max con h compatible
    ### v max
    bbve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j1(h,st.session_state.v,'exterior')
    hbve = h + hRv(h,st.session_state.RV) + Va2(h,OBS)
    PAbve = [bbve,hbve]
    ### v = 0
    bb0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j1(h,st.session_state.v,'exterior')
    hb0e = h + hRv(h,st.session_state.RV) + Va2(h,OBS)
    PAb0e = [bb0e,hb0e]
    ## h max con b compatible
    ### v max
    bhve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j1_bis(h,st.session_state.v,'exterior')
    hhve = h + hRv(h,st.session_state.RV) + Va2_bis(h,OBS)
    PAhve = [bhve,hhve]
    ### v = 0
    bh0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j1_bis(h,st.session_state.v,'exterior')
    hh0e = h + hRv(h,st.session_state.RV) + Va2_bis(h,OBS)
    PAh0e = [bh0e,hh0e]
    #print(PAbvi,PAbve)
    #print(PAb0i,PAb0e)
    #print(PAhvi,PAhve)
    #print(PAh0i,PAh0e)
    return PAbvi,PAbve,PAb0i,PAb0e,PAhvi,PAhve,PAh0i,PAh0e

##Partes altas: puntos por debajo de la anchura máxima
def PA_below(b,h):
    #Lado interior
    ## b max con h compatible
    ### v max
    bbvi = b + Si_a(h,st.session_state.r)[0]  - qSIi_a(h,st.session_state.i)[0] + j1(h,st.session_state.v,'interior')
    hbvi = h - hRv(h,st.session_state.RV) - Vi2(h,OBS)
    PAbvi = [-bbvi,hbvi]
    ### v = 0
    bb0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j1(h,st.session_state.v,'interior')
    hb0i = h - hRv(h,st.session_state.RV) - Vi2(h,OBS)
    PAb0i = [-bb0i,hb0i]
    ## h max con b compatible
    ### v max
    bhvi = b + Si_a(h,st.session_state.r)[0] - qSIi_a(h,st.session_state.i)[0] + j1_bis(h,st.session_state.v,'interior')
    hhvi = h - hRv(h,st.session_state.RV) - Vi2_bis(h,OBS)
    PAhvi = [-bhvi,hhvi]
    ### v = 0
    bh0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j1_bis(h,st.session_state.v,'interior')
    hh0i = h - hRv(h,st.session_state.RV) - Vi2_bis(h,OBS)
    PAh0i = [-bh0i,hh0i]
    #Lado exterior
    ## b max con h compatible
    ### v max
    bbve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j1(h,st.session_state.v,'exterior')
    hbve = h - hRv(h,st.session_state.RV) - Va2(h,OBS)
    PAbve = [bbve,hbve]
    ### v = 0
    bb0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j1(h,st.session_state.v,'exterior')
    hb0e = h - hRv(h,st.session_state.RV) - Va2(h,OBS)
    PAb0e = [bb0e,hb0e]
    ## h max con b compatible
    ### v max
    bhve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j1_bis(h,st.session_state.v,'exterior')
    hhve = h - hRv(h,st.session_state.RV) - Va2_bis(h,OBS)
    PAhve = [bhve,hhve]
    ### v = 0
    bh0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j1_bis(h,st.session_state.v,'exterior')
    hh0e = h - hRv(h,st.session_state.RV) - Va2_bis(h,OBS)
    PAh0e = [bh0e,hh0e]
    #print(PAbvi,PAbve)
    #print(PAb0i,PAb0e)
    #print(PAhvi,PAhve)
    #print(PAh0i,PAh0e)
    return PAbvi,PAbve,PAb0i,PAb0e,PAhvi,PAhve,PAh0i,PAh0e

##Pates bajas
def PB(b,h):
    #Lado interior
    ## b max con h compatible
    ### v max
    bbvi = b + Si_a(h,st.session_state.r)[0] + j2(h,st.session_state.v)
    hbvi = h - hRv(h,st.session_state.RV) - Vi2(h,OBS)
    PAbvi = [-bbvi,hbvi]
    ### v = 0
    bb0i = b + Si_a(h,st.session_state.r)[0] + j2(h,st.session_state.v)
    hb0i = h - hRv(h,st.session_state.RV) - Vi2(h,OBS)
    PAb0i = [-bb0i,hb0i]
    ## h max con b compatible
    ### v max
    bhvi = b + Si_a(h,st.session_state.r)[0] + j2_bis(h,st.session_state.v)
    hhvi = h - hRv(h,st.session_state.RV) - Vi2_bis(h,OBS)
    PAhvi = [-bhvi,hhvi]
    ### v = 0
    bh0i = b + Si_a(h,st.session_state.r)[0] + j2_bis(h,st.session_state.v)
    hh0i = h - hRv(h,st.session_state.RV) - Vi2_bis(h,OBS)
    PAh0i = [-bh0i,hh0i]
    #Lado exterior
    ## b max con h compatible
    ### v max
    bbve = b + Si_a(h,st.session_state.r)[1] + j2(h,st.session_state.v)
    hbve = h - hRv(h,st.session_state.RV) - Va2(h,OBS)
    PAbve = [bbve,hbve]
    ### v = 0
    bb0e = b + Si_a(h,st.session_state.r)[1] + j2(h,st.session_state.v)
    hb0e = h - hRv(h,st.session_state.RV) - Va2(h,OBS)
    PAb0e = [bb0e,hb0e]
    ## h max con b compatible
    ### v max
    bhve = b + Si_a(h,st.session_state.r)[1] + j2_bis(h,st.session_state.v)
    hhve = h - hRv(h,st.session_state.RV) - Va2_bis(h,OBS)
    PAhve = [bhve,hhve]
    ### v = 0
    bh0e = b + Si_a(h,st.session_state.r)[1] + j2_bis(h,st.session_state.v)
    hh0e = h - hRv(h,st.session_state.RV) - Va2_bis(h,OBS)
    PAh0e = [bh0e,hh0e]
    #print(PAbvi,PAbve)
    #print(PAb0i,PAb0e)
    #print(PAhvi,PAhve)
    #print(PAh0i,PAh0e)
    return PAbvi,PAbve,PAb0i,PAb0e,PAhvi,PAhve,PAh0i,PAh0e

#GÁLIBO NOMINAL DE IMPLANTACIÓN DE OBSTÁCULOS

##Punto PT
def PT_nominal(b,h):
    #Lado interior
    ## b max con h compatible
    ### v max
    bbvi = b +  Si_a(h,st.session_state.r)[0] - qSIi_a(h,st.session_state.i)[0] + j3(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hbvi = h + hRv(h,st.session_state.RV) + hPTIi_a(h,st.session_state.i)[0] +Vi3(h,bPT,st.session_state.v,'exterior',OBS) + M3b_h(h)[1]
    PTbvi = [-bbvi,hbvi]
    ### v = 0
    bb0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j3(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hb0i = h + hRv(h,st.session_state.RV) - hPTDi_a(h,st.session_state.d)[0] + Vi3(h,bPT,st.session_state.v,'exterior',OBS) + M3b_h(h)[1]
    PTb0i = [-bb0i,hb0i]
    ## h max con b compatible
    ### v max
    bhvi = b + Si_a(h,st.session_state.r)[0] - qSIi_a(h,st.session_state.i)[0] + j3_bis(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hhvi = h + hRv(h,st.session_state.RV) + hPTIi_a(h,st.session_state.i)[0] + Vi3_bis(h,bPT,st.session_state.v,'exterior',OBS) + M3b_h(h)[1]
    PThvi = [-bhvi,hhvi]
    ### v = 0
    bh0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j3_bis(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hh0i = h + hRv(h,st.session_state.RV) - hPTDi_a(h,st.session_state.d)[0] + Vi3_bis(h,bPT,st.session_state.v,'exterior',OBS) + M3b_h(h)[1]
    PTh0i = [-bh0i,hh0i]
    #Lado exterior
    ## b max con h compatible
    ### v max
    bbve = b +  Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j3(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hbve = h + hRv(h,st.session_state.RV) - hPTIi_a(h,st.session_state.i)[1] + Va3(h,bPT,st.session_state.v,'interior',OBS) + M3b_h(h)[1]
    PTbve = [bbve,hbve]
    ### v = 0
    bb0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j3(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hb0e = h + hRv(h,st.session_state.RV) + hPTDi_a(h,st.session_state.d)[1] + Va3(h,bPT,st.session_state.v,'interior',OBS) + M3b_h(h)[1]
    PTb0e = [bb0e,hb0e]
    ## h max con b compatible
    ### v max
    bhve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j3_bis(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hhve = h + hRv(h,st.session_state.RV) - hPTIi_a(h,st.session_state.i)[1] + Va3_bis(h,bPT,st.session_state.v,'interior',OBS) + M3b_h(h)[1]
    PThve = [bhve,hhve]
    ### v = 0
    bh0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j3_bis(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hh0e = h + hRv(h,st.session_state.RV) + hPTDi_a(h,st.session_state.d)[1] + Va3_bis(h,bPT,st.session_state.v,'interior',OBS) + M3b_h(h)[1]
    PTh0e = [bh0e,hh0e]
    #print(PTbvi,PTbve)
    #print(PTb0i,PTb0e)
    #print(PThvi,PThve)
    #print(PTh0i,PTh0e)
    return PTbvi,PTbve,PTb0i,PTb0e,PThvi,PThve,PTh0i,PTh0e

##Partes altas: puntos por encima de la anchura máxima
def PA_above_nominal(b,h):
    #Lado interior
    ## b max con h compatible
    ### v max
    bbvi = b + Si_a(h,st.session_state.r)[0]  - qSIi_a(h,st.session_state.i)[0] + j3(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hbvi = h + hRv(h,st.session_state.RV) + Vi4(h,OBS) + M3b_h(h)[1]
    PAbvi = [-bbvi,hbvi]
    ### v = 0
    bb0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j3(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hb0i = h + hRv(h,st.session_state.RV) + Vi4(h,OBS) + M3b_h(h)[1]
    PAb0i = [-bb0i,hb0i]
    ## h max con b compatible
    ### v max
    bhvi = b + Si_a(h,st.session_state.r)[0] - qSIi_a(h,st.session_state.i)[0] + j3_bis(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hhvi = h + hRv(h,st.session_state.RV) + Vi4_bis(h,OBS) + M3b_h(h)[1]
    PAhvi = [-bhvi,hhvi]
    ### v = 0
    bh0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j3_bis(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hh0i = h + hRv(h,st.session_state.RV) + Vi4_bis(h,OBS) + M3b_h(h)[1]
    PAh0i = [-bh0i,hh0i]
    #Lado exterior
    ## b max con h compatible
    ### v max
    bbve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j3(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hbve = h + hRv(h,st.session_state.RV) + Va4(h,OBS) + M3b_h(h)[1]
    PAbve = [bbve,hbve]
    ### v = 0
    bb0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j3(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hb0e = h + hRv(h,st.session_state.RV) + Va4(h,OBS) + M3b_h(h)[1]
    PAb0e = [bb0e,hb0e]
    ## h max con b compatible
    ### v max
    bhve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j3_bis(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hhve = h + hRv(h,st.session_state.RV) + Va4_bis(h,OBS) + M3b_h(h)[1]
    PAhve = [bhve,hhve]
    ### v = 0
    bh0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j3_bis(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hh0e = h + hRv(h,st.session_state.RV) + Va4_bis(h,OBS) + M3b_h(h)[1]
    PAh0e = [bh0e,hh0e]
    #print(PAbvi,PAbve)
    #print(PAb0i,PAb0e)
    #print(PAhvi,PAhve)
    #print(PAh0i,PAh0e)
    return PAbvi,PAbve,PAb0i,PAb0e,PAhvi,PAhve,PAh0i,PAh0e

##Partes altas: puntos por debajo de la anchura máxima
def PA_below_nominal(b,h):
    #Lado interior
    ## b max con h compatible
    ### v max
    bbvi = b + Si_a(h,st.session_state.r)[0]  - qSIi_a(h,st.session_state.i)[0] + j3(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hbvi = h - hRv(h,st.session_state.RV) - Vi4(h,OBS) - M3b_h(h)[1]
    PAbvi = [-bbvi,hbvi]
    ### v = 0
    bb0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j3(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hb0i = h - hRv(h,st.session_state.RV) - Vi4(h,OBS) - M3b_h(h)[1]
    PAb0i = [-bb0i,hb0i]
    ## h max con b compatible
    ### v max
    bhvi = b + Si_a(h,st.session_state.r)[0] - qSIi_a(h,st.session_state.i)[0] + j3_bis(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hhvi = h - hRv(h,st.session_state.RV) - Vi4_bis(h,OBS) - M3b_h(h)[1]
    PAhvi = [-bhvi,hhvi]
    ### v = 0
    bh0i = b + Si_a(h,st.session_state.r)[0] + qSDi_a(h,st.session_state.d)[0] + j3_bis(h,st.session_state.v,'interior') + M3b_h(h)[0]
    hh0i = h - hRv(h,st.session_state.RV) - Vi4_bis(h,OBS) - M3b_h(h)[1]
    PAh0i = [-bh0i,hh0i]
    #Lado exterior
    ## b max con h compatible
    ### v max
    bbve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j3(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hbve = h - hRv(h,st.session_state.RV) - Va4(h,OBS) - M3b_h(h)[1]
    PAbve = [bbve,hbve]
    ### v = 0
    bb0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j3(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hb0e = h - hRv(h,st.session_state.RV) - Va4(h,OBS) - M3b_h(h)[1]
    PAb0e = [bb0e,hb0e]
    ## h max con b compatible
    ### v max
    bhve = b + Si_a(h,st.session_state.r)[1] + qSIi_a(h,st.session_state.i)[1] + j3_bis(h,st.session_state.v,'exterior') + M3b_h(h)[0]
    hhve = h - hRv(h,st.session_state.RV) - Va4_bis(h,OBS) - M3b_h(h)[1]
    PAhve = [bhve,hhve]
    ### v = 0
    bh0e = b + Si_a(h,st.session_state.r)[1] - qSDi_a(h,st.session_state.d)[1] + j3_bis(h,st.session_state.v,'exterior') +M3b_h(h)[0]
    hh0e = h - hRv(h,st.session_state.RV) - Va4_bis(h,OBS) - M3b_h(h)[1]
    PAh0e = [bh0e,hh0e]
    #print(PAbvi,PAbve)
    #print(PAb0i,PAb0e)
    #print(PAhvi,PAhve)
    #print(PAh0i,PAh0e)
    return PAbvi,PAbve,PAb0i,PAb0e,PAhvi,PAhve,PAh0i,PAh0e

##Pates bajas
def PB_nominal(b,h):
    #Lado interior
    ## b max con h compatible
    ### v max
    bbvi = b + Si_a(h,st.session_state.r)[0] + j4(h,st.session_state.v) + M3b_h(h)[0]
    hbvi = h - hRv(h,st.session_state.RV) - Vi4(h,OBS) - M3b_h(h)[1]
    PAbvi = [-bbvi,hbvi]
    ### v = 0
    bb0i = b + Si_a(h,st.session_state.r)[0] + j4(h,st.session_state.v) + M3b_h(h)[0]
    hb0i = h - hRv(h,st.session_state.RV) - Vi4(h,OBS) - M3b_h(h)[1]
    PAb0i = [-bb0i,hb0i]
    ## h max con b compatible
    ### v max
    bhvi = b + Si_a(h,st.session_state.r)[0] + j4_bis(h,st.session_state.v) + M3b_h(h)[0]
    hhvi = h - hRv(h,st.session_state.RV) - Vi4_bis(h,OBS) - M3b_h(h)[1]
    PAhvi = [-bhvi,hhvi]
    ### v = 0
    bh0i = b + Si_a(h,st.session_state.r)[0] + j4_bis(h,st.session_state.v) + M3b_h(h)[0]
    hh0i = h - hRv(h,st.session_state.RV) - Vi4_bis(h,OBS) - M3b_h(h)[1]
    PAh0i = [-bh0i,hh0i]
    #Lado exterior
    ## b max con h compatible
    ### v max
    bbve = b + Si_a(h,st.session_state.r)[1] + j4(h,st.session_state.v) + M3b_h(h)[0]
    hbve = h - hRv(h,st.session_state.RV) - Va4(h,OBS) - M3b_h(h)[1]
    PAbve = [bbve,hbve]
    ### v = 0
    bb0e = b + Si_a(h,st.session_state.r)[1] + j4(h,st.session_state.v) + M3b_h(h)[0]
    hb0e = h - hRv(h,st.session_state.RV) - Va4(h,OBS) - M3b_h(h)[1]
    PAb0e = [bb0e,hb0e]
    ## h max con b compatible
    ### v max
    bhve = b + Si_a(h,st.session_state.r)[1] + j4_bis(h,st.session_state.v) + M3b_h(h)[0]
    hhve = h - hRv(h,st.session_state.RV) - Va4_bis(h,OBS) - M3b_h(h)[1]
    PAhve = [bhve,hhve]
    ### v = 0
    bh0e = b + Si_a(h,st.session_state.r)[1] + j4_bis(h,st.session_state.v) + M3b_h(h)[0]
    hh0e = h - hRv(h,st.session_state.RV) - Va4_bis(h,OBS) - M3b_h(h)[1]
    PAh0e = [bh0e,hh0e]
    #print(PAbvi,PAbve)
    #print(PAb0i,PAb0e)
    #print(PAhvi,PAhve)
    #print(PAh0i,PAh0e)
    return PAbvi,PAbve,PAb0i,PAb0e,PAhvi,PAhve,PAh0i,PAh0e

#Definición gálibos límite
def gal_limite(contorno):
    gal_bvi = [[0,0]] * len(puntos)
    gal_bve = [[0,0]] * len(puntos)
    gal_b0i = [[0,0]] * len(puntos)
    gal_b0e = [[0,0]] * len(puntos)
    gal_hvi = [[0,0]] * len(puntos)
    gal_hve = [[0,0]] * len(puntos)
    gal_h0i = [[0,0]] * len(puntos)
    gal_h0e = [[0,0]] * len(puntos)
    n = 0
    m = len(contorno) - 1
    for punto in contorno:
        if punto[1] == hPT:
            gal_bvi[n] = PT(punto[0],punto[1])[0]
            gal_bve[m-n] = PT(punto[0],punto[1])[1]
            gal_b0i[n] = PT(punto[0],punto[1])[2]
            gal_b0e[m-n] = PT(punto[0],punto[1])[3]
            gal_hvi[n] = PT(punto[0],punto[1])[4]
            gal_hve[m-n] = PT(punto[0],punto[1])[5]
            gal_h0i[n] = PT(punto[0],punto[1])[6]
            gal_h0e[m-n] = PT(punto[0],punto[1])[7]
        elif punto[1] >= st.session_state.hPT_max:
            gal_bvi[n] = PA_above(punto[0],punto[1])[0]
            gal_bve[m-n] = PA_above(punto[0],punto[1])[1]
            gal_b0i[n] = PA_above(punto[0],punto[1])[2]
            gal_b0e[m-n] = PA_above(punto[0],punto[1])[3]
            gal_hvi[n] = PA_above(punto[0],punto[1])[4]
            gal_hve[m-n] = PA_above(punto[0],punto[1])[5]
            gal_h0i[n] = PA_above(punto[0],punto[1])[6]
            gal_h0e[m-n] = PA_above(punto[0],punto[1])[7]
        elif punto[1] <= hPT_min:
            gal_bvi[n] = PA_below(punto[0],punto[1])[0]
            gal_bve[m-n] = PA_below(punto[0],punto[1])[1]
            gal_b0i[n] = PA_below(punto[0],punto[1])[2]
            gal_b0e[m-n] = PA_below(punto[0],punto[1])[3]
            gal_hvi[n] = PA_below(punto[0],punto[1])[4]
            gal_hve[m-n] = PA_below(punto[0],punto[1])[5]
            gal_h0i[n] = PA_below(punto[0],punto[1])[6]
            gal_h0e[m-n] = PA_below(punto[0],punto[1])[7]
        elif punto[1] <= 0.4:
            gal_bvi[n] = PB(punto[0],punto[1])[0]
            gal_bve[m-n] = PB(punto[0],punto[1])[1]
            gal_b0i[n] = PB(punto[0],punto[1])[2]
            gal_b0e[m-n] = PB(punto[0],punto[1])[3]
            gal_hvi[n] = PB(punto[0],punto[1])[4]
            gal_hve[m-n] = PB(punto[0],punto[1])[5]
            gal_h0i[n] = PB(punto[0],punto[1])[6]
            gal_h0e[m-n] = PB(punto[0],punto[1])[7]
        n += 1
    #Generación gálibos según casos particulares
    gal_bv = gal_bvi + gal_bve
    gal_b0 = gal_b0i + gal_b0e
    gal_hv = gal_hvi + gal_hve
    gal_h0 = gal_h0i + gal_h0e
    #Generación gálibo límite según casos particulares
    gal_bv = np.array(gal_bv)
    gal_b0 = np.array(gal_b0)
    gal_hv = np.array(gal_hv)
    gal_h0 = np.array(gal_h0)
    bf = pd.DataFrame({'b max con h compatible v=vmax (b)':gal_bv[:,0],
                       'b max con h compatible v=0 (b)':gal_b0[:,0],
                       'h max con b compatible v=vmax (b)':gal_hv[:,0],
                       'h max con b compatible v=0 (b)':gal_h0[:,0]})
    hf = pd.DataFrame({'b max con h compatbiel v =vmax (h)':gal_bv[:,1],
                       'b max con h compatible v=0 (h)':gal_b0[:,1],
                       'h max con b compatible v=vmax (h)':gal_hv[:,1],
                       'h max con b compatible v=0 (h)':gal_h0[:,1]})
    df = pd.DataFrame({'b max con h compatible v=vmax (b)':gal_bv[:,0], 'b max con h compatbiel v =vmax (h)':gal_bv[:,1],
                       'b max con h compatible v=0 (b)':gal_b0[:,0], 'b max con h compatible v=0 (h)':gal_b0[:,1],
                       'h max con b compatible v=vmax (b)':gal_hv[:,0], 'h max con b compatible v=vmax (h)':gal_hv[:,1],
                       'h max con b compatible v=0 (b)':gal_h0[:,0], 'h max con b compatible v=0 (h)':gal_h0[:,1]})
    gf = pd.DataFrame({'b max con h compatible v=vmax (b)':gal_bv[:,0], 'b max con h compatbiel v =vmax (h)':gal_bv[:,1],
                       'b max con h compatible v=0 (b)':gal_b0[:,0], 'b max con h compatible v=0 (h)':gal_b0[:,1],
                       'h max con b compatible v=vmax (b)':gal_hv[:,0], 'h max con b compatible v=vmax (h)':gal_hv[:,1],
                       'h max con b compatible v=0 (b)':gal_h0[:,0], 'h max con b compatible v=0 (h)':gal_h0[:,1]})
    bf['Gálibo límite (b) exterior'] = bf.max(axis=1)
    bf['Gálibo límite (b) interior'] = bf.min(axis=1)
    bf['Gálibo límite (b)'] = 0
    hf['Gálibo límite (h) superior'] = hf.max(axis=1)
    hf['Gálibo límite (h) inferior'] = hf.min(axis=1)
    hf['Gálibo límite (h)'] = 0
    df['norm_gal_bv'] = np.linalg.norm([df['b max con h compatible v=vmax (b)'],df['b max con h compatbiel v =vmax (h)']],axis=0)
    df['norm_gal_b0'] = np.linalg.norm([df['b max con h compatible v=0 (b)'],df['b max con h compatible v=0 (h)']],axis=0)
    df['norm_gal_hv'] = np.linalg.norm([df['h max con b compatible v=vmax (b)'],df['h max con b compatible v=vmax (h)']],axis=0)
    df['norm_gal_h0'] = np.linalg.norm([df['h max con b compatible v=0 (b)'],df['h max con b compatible v=0 (h)']],axis=0)
    MAX = df[['norm_gal_bv','norm_gal_b0','norm_gal_hv','norm_gal_h0']].max(axis=1)
    df['norm_gal_lim'] = MAX
    df['Gálibo límite (b)'] = 0
    df['Gálibo límite (h)'] = 0
    #gf['Gálibo límite (b)'] = 0
    #gf['Gálibo límite (h)'] = 0
    k = 0
    #for k in range(len(gf)):
        #aux_b_int = bf['Gálibo límite (b) interior'][k]
        #aux_b_ext = bf['Gálibo límite (b) exterior'][k]
        #aux_h_inf = hf['Gálibo límite (h) inferior'][k]
        #aux_h_sup = hf['Gálibo límite (h) superior'][k]
        #if aux_b_int > 0 and aux_h_inf > 0:
            #gf.loc[[k],['Gálibo límite (b)']] = aux_b_ext
            #gf.loc[[k],['Gálibo límite (h)']] = aux_h_sup
            #bf.loc[[k],['Gálibo límite (b)']] = aux_b_ext
            #hf.loc[[k],['Gálibo límite (h)']] = aux_h_sup
            #n += 1
        #elif aux_b_int > 0 and aux_h_inf < 0:
            #gf.loc[[k],['Gálibo límite (b)']] = aux_b_ext
            #gf.loc[[k],['Gálibo límite (h)']] = aux_h_inf
            #bf.loc[[k],['Gálibo límite (b)']] = aux_b_ext
            #hf.loc[[k],['Gálibo límite (h)']] = aux_h_inf
            #n += 1
        #elif aux_b_int < 0 and aux_h_inf > 0:
            #gf.loc[[k],['Gálibo límite (b)']] = aux_b_int
            #gf.loc[[k],['Gálibo límite (h)']] = aux_h_sup
            #bf.loc[[k],['Gálibo límite (b)']] = aux_b_int
            #hf.loc[[k],['Gálibo límite (h)']] = aux_h_sup
            #n += 1
        #elif aux_b_int < 0 and aux_h_inf < 0:
            #gf.loc[[k],['Gálibo límite (b)']] = aux_b_int
            #gf.loc[[k],['Gálibo límite (h)']] = aux_h_inf
            #bf.loc[[k],['Gálibo límite (b)']] = aux_b_int
            #hf.loc[[k],['Gálibo límite (h)']] = aux_h_inf
            #n += 1
    return gal_bv,gal_b0,gal_hv,gal_h0, df, bf, hf, gf

#Definición gálibos nominal
def gal_nominal(contorno):
    gal_bvi = [[0,0]] * len(puntos)
    gal_bve = [[0,0]] * len(puntos)
    gal_b0i = [[0,0]] * len(puntos)
    gal_b0e = [[0,0]] * len(puntos)
    gal_hvi = [[0,0]] * len(puntos)
    gal_hve = [[0,0]] * len(puntos)
    gal_h0i = [[0,0]] * len(puntos)
    gal_h0e = [[0,0]] * len(puntos)
    n = 0
    m = len(contorno) - 1
    for punto in contorno:
        if punto[1] == hPT:
            gal_bvi[n] = PT_nominal(punto[0],punto[1])[0]
            gal_bve[m-n] = PT_nominal(punto[0],punto[1])[1]
            gal_b0i[n] = PT_nominal(punto[0],punto[1])[2]
            gal_b0e[m-n] = PT_nominal(punto[0],punto[1])[3]
            gal_hvi[n] = PT_nominal(punto[0],punto[1])[4]
            gal_hve[m-n] = PT_nominal(punto[0],punto[1])[5]
            gal_h0i[n] = PT_nominal(punto[0],punto[1])[6]
            gal_h0e[m-n] = PT_nominal(punto[0],punto[1])[7]
        elif punto[1] >= st.session_state.hPT_max:
            gal_bvi[n] = PA_above_nominal(punto[0],punto[1])[0]
            gal_bve[m-n] = PA_above_nominal(punto[0],punto[1])[1]
            gal_b0i[n] = PA_above_nominal(punto[0],punto[1])[2]
            gal_b0e[m-n] = PA_above_nominal(punto[0],punto[1])[3]
            gal_hvi[n] = PA_above_nominal(punto[0],punto[1])[4]
            gal_hve[m-n] = PA_above_nominal(punto[0],punto[1])[5]
            gal_h0i[n] = PA_above_nominal(punto[0],punto[1])[6]
            gal_h0e[m-n] = PA_above_nominal(punto[0],punto[1])[7]
        elif punto[1] <= hPT_min:
            gal_bvi[n] = PA_below_nominal(punto[0],punto[1])[0]
            gal_bve[m-n] = PA_below_nominal(punto[0],punto[1])[1]
            gal_b0i[n] = PA_below_nominal(punto[0],punto[1])[2]
            gal_b0e[m-n] = PA_below_nominal(punto[0],punto[1])[3]
            gal_hvi[n] = PA_below_nominal(punto[0],punto[1])[4]
            gal_hve[m-n] = PA_below_nominal(punto[0],punto[1])[5]
            gal_h0i[n] = PA_below_nominal(punto[0],punto[1])[6]
            gal_h0e[m-n] = PA_below_nominal(punto[0],punto[1])[7]
        elif punto[1] <= 0.4:
            gal_bvi[n] = PB_nominal(punto[0],punto[1])[0]
            gal_bve[m-n] = PB_nominal(punto[0],punto[1])[1]
            gal_b0i[n] = PB_nominal(punto[0],punto[1])[2]
            gal_b0e[m-n] = PB_nominal(punto[0],punto[1])[3]
            gal_hvi[n] = PB_nominal(punto[0],punto[1])[4]
            gal_hve[m-n] = PB_nominal(punto[0],punto[1])[5]
            gal_h0i[n] = PB_nominal(punto[0],punto[1])[6]
            gal_h0e[m-n] = PB_nominal(punto[0],punto[1])[7]
        n += 1
    #Generación gálibos según casos particulares
    gal_bv = gal_bvi + gal_bve
    gal_b0 = gal_b0i + gal_b0e
    gal_hv = gal_hvi + gal_hve
    gal_h0 = gal_h0i + gal_h0e
    #Generación gálibo límite según casos particulares
    gal_bv = np.array(gal_bv)
    gal_b0 = np.array(gal_b0)
    gal_hv = np.array(gal_hv)
    gal_h0 = np.array(gal_h0)
    bf = pd.DataFrame({'b max con h compatible v=vmax (b)':gal_bv[:,0],
                       'b max con h compatible v=0 (b)':gal_b0[:,0],
                       'h max con b compatible v=vmax (b)':gal_hv[:,0],
                       'h max con b compatible v=0 (b)':gal_h0[:,0]})
    hf = pd.DataFrame({'b max con h compatbiel v =vmax (h)':gal_bv[:,1],
                       'b max con h compatible v=0 (h)':gal_b0[:,1],
                       'h max con b compatible v=vmax (h)':gal_hv[:,1],
                       'h max con b compatible v=0 (h)':gal_h0[:,1]})
    df = pd.DataFrame({'b max con h compatible v=vmax (b)':gal_bv[:,0], 'b max con h compatbiel v =vmax (h)':gal_bv[:,1],
                       'b max con h compatible v=0 (b)':gal_b0[:,0], 'b max con h compatible v=0 (h)':gal_b0[:,1],
                       'h max con b compatible v=vmax (b)':gal_hv[:,0], 'h max con b compatible v=vmax (h)':gal_hv[:,1],
                       'h max con b compatible v=0 (b)':gal_h0[:,0], 'h max con b compatible v=0 (h)':gal_h0[:,1]})
    gf = pd.DataFrame({'b max con h compatible v=vmax (b)':gal_bv[:,0], 'b max con h compatbiel v =vmax (h)':gal_bv[:,1],
                       'b max con h compatible v=0 (b)':gal_b0[:,0], 'b max con h compatible v=0 (h)':gal_b0[:,1],
                       'h max con b compatible v=vmax (b)':gal_hv[:,0], 'h max con b compatible v=vmax (h)':gal_hv[:,1],
                       'h max con b compatible v=0 (b)':gal_h0[:,0], 'h max con b compatible v=0 (h)':gal_h0[:,1]})
    bf['Gálibo límite (b) exterior'] = bf.max(axis=1)
    bf['Gálibo límite (b) interior'] = bf.min(axis=1)
    bf['Gálibo límite (b)'] = 0
    hf['Gálibo límite (h) superior'] = hf.max(axis=1)
    hf['Gálibo límite (h) inferior'] = hf.min(axis=1)
    hf['Gálibo límite (h)'] = 0
    df['norm_gal_bv'] = np.linalg.norm([df['b max con h compatible v=vmax (b)'],df['b max con h compatbiel v =vmax (h)']],axis=0)
    df['norm_gal_b0'] = np.linalg.norm([df['b max con h compatible v=0 (b)'],df['b max con h compatible v=0 (h)']],axis=0)
    df['norm_gal_hv'] = np.linalg.norm([df['h max con b compatible v=vmax (b)'],df['h max con b compatible v=vmax (h)']],axis=0)
    df['norm_gal_h0'] = np.linalg.norm([df['h max con b compatible v=0 (b)'],df['h max con b compatible v=0 (h)']],axis=0)
    MAX = df[['norm_gal_bv','norm_gal_b0','norm_gal_hv','norm_gal_h0']].max(axis=1)
    df['norm_gal_lim'] = MAX
    df['Gálibo límite (b)'] = 0
    df['Gálibo límite (h)'] = 0
    #gf['Gálibo límite (b)'] = 0
    #gf['Gálibo límite (h)'] = 0
    k = 0
    #for k in range(len(gf)):
        #aux_b_int = bf['Gálibo límite (b) interior'][k]
        #aux_b_ext = bf['Gálibo límite (b) exterior'][k]
        #aux_h_inf = hf['Gálibo límite (h) inferior'][k]
        #aux_h_sup = hf['Gálibo límite (h) superior'][k]
        #if aux_b_int > 0 and aux_h_inf > 0:
            #gf.loc[[k],['Gálibo límite (b)']] = aux_b_ext
            #gf.loc[[k],['Gálibo límite (h)']] = aux_h_sup
            #bf.loc[[k],['Gálibo límite (b)']] = aux_b_ext
            #hf.loc[[k],['Gálibo límite (h)']] = aux_h_sup
            #n += 1
        #elif aux_b_int > 0 and aux_h_inf < 0:
            #gf.loc[[k],['Gálibo límite (b)']] = aux_b_ext
            #gf.loc[[k],['Gálibo límite (h)']] = aux_h_inf
            #bf.loc[[k],['Gálibo límite (b)']] = aux_b_ext
            #hf.loc[[k],['Gálibo límite (h)']] = aux_h_inf
            #n += 1
        #elif aux_b_int < 0 and aux_h_inf > 0:
            #gf.loc[[k],['Gálibo límite (b)']] = aux_b_int
            #gf.loc[[k],['Gálibo límite (h)']] = aux_h_sup
            #bf.loc[[k],['Gálibo límite (b)']] = aux_b_int
            #hf.loc[[k],['Gálibo límite (h)']] = aux_h_sup
            #n += 1
        #elif aux_b_int < 0 and aux_h_inf < 0:
            #gf.loc[[k],['Gálibo límite (b)']] = aux_b_int
            #gf.loc[[k],['Gálibo límite (h)']] = aux_h_inf
            #bf.loc[[k],['Gálibo límite (b)']] = aux_b_int
            #hf.loc[[k],['Gálibo límite (h)']] = aux_h_inf
            #n += 1
    return gal_bv,gal_b0,gal_hv,gal_h0, df, bf, hf, gf

def obtener_inputs():
    d = st.session_state.d
    i = st.session_state.i
    r = st.session_state.r
    RV = st.session_state.RV
    v = st.session_state.v / 1000 * 3600
    df_input = pd.DataFrame({'Peralte máximo (mm)':[d], 'Insuficiencia de peralte máximo (mm)': [i],
    'Radio mínimo en planta (m)': [r], 'Radio mínimo acuerdo vertical (m)': [RV], 'Velocidad máxima de circulación (km/h)':[v]})
    return df_input

def obtener_variables_unicas(v,obs):
    tvia = Tvia()
    td = TD(v)
    alphac = alpha_c*180/pi
    alphasusp = alpha_susp*180/pi
    kbis = K_bis
    pf = pd.DataFrame({'Tvia(m)':[tvia], 'TD(m)':[td], 'α_c (º)':[alphac], 'α_susp(º)':[alphasusp], "K'":[kbis]})
    return pf

def obtener_variables_contorno(contorno):
    Siv = [0] * len(puntos)
    Sav = [0] * len(puntos)
    qSDiv = [0]*len(puntos)
    qSIiv = [0]*len(puntos)
    qSDav = [0]*len(puntos)
    qSIav = [0]*len(puntos)
    j1iv = [0]*len(puntos)
    j1i_bisv = [0]*len(puntos)
    j2iv = [0]*len(puntos)
    j2i_bisv = [0]*len(puntos)
    j3iv = [0]*len(puntos)
    j3i_bisv = [0]*len(puntos)
    j4iv = [0]*len(puntos)
    j4i_bisv = [0]*len(puntos)
    Vi1v = [0]*len(puntos)
    Vi_bis1v = [0]*len(puntos)
    Vi2v = [0]*len(puntos)
    Vi_bis2v = [0]*len(puntos)
    Vi3v = [0]*len(puntos)
    Vi_bis3v = [0]*len(puntos)
    Vi4v = [0]*len(puntos)
    Vi_bis4v = [0]*len(puntos)
    j1av = [0]*len(puntos)
    j1a_bisv = [0]*len(puntos)
    j2av = [0]*len(puntos)
    j2a_bisv = [0]*len(puntos)
    j3av = [0]*len(puntos)
    j3a_bisv = [0]*len(puntos)
    j4av = [0]*len(puntos)
    j4a_bisv = [0]*len(puntos)
    Va1v = [0]*len(puntos)
    Va_bis1v = [0]*len(puntos)
    Va2v = [0]*len(puntos)
    Va_bis2v = [0]*len(puntos)
    Va3v = [0]*len(puntos)
    Va_bis3v = [0]*len(puntos)
    Va4v = [0]*len(puntos)
    Va_bis4v = [0]*len(puntos)
    alphaosci = [0]*len(puntos)
    alphaosca = [0]*len(puntos)
    tnv = [0]*len(puntos)
    kv = [0]*len(puntos)

    n = 0
    m = len(contorno) - 1
    for punto in contorno:
            Siv[n] = Si_a(punto[0],st.session_state.r)[0]
            Sav[n] = Si_a(punto[0],st.session_state.r)[1]
            qSDiv[n] = qSDi_a(punto[0],st.session_state.d)[0]
            qSIiv[n] = qSIi_a(punto[0],st.session_state.i)[0]
            qSDav[n] = qSDi_a(punto[0],st.session_state.d)[0]
            qSIav[n] = qSIi_a(punto[0],st.session_state.i)[0]
            j1iv[n] = j1(punto[0],st.session_state.v,'interior')
            j1av[n] = j1(punto[0],st.session_state.v,'exterior')
            j1i_bisv[n] = j1_bis(punto[0],st.session_state.v,'interior')
            j1a_bisv[n] = j1_bis(punto[0],st.session_state.v,'exterior')
            j2iv[n] = j2(punto[0],st.session_state.v)
            j2av[n] = j2iv[n]
            j2i_bisv[n] = j2_bis(punto[0],st.session_state.v)
            j2a_bisv[n] = j2i_bisv[n]
            j3iv[n] = j3(punto[0],st.session_state.v,'interior')
            j3av[n] = j3(punto[0],st.session_state.v,'exterior')
            j3i_bisv[n] = j3_bis(punto[0],st.session_state.v,'interior')
            j3a_bisv[n] = j3_bis(punto[0],st.session_state.v,'exterior')
            j4iv[n] = j4(punto[0],st.session_state.v)
            j4av[n] = j4iv[n]
            Vi1v[n] = Vi1(punto[0],st.session_state.v,'interior',OBS)
            Va1v[n] = Va1(punto[0],st.session_state.v,'exterior',OBS)
            Vi_bis1v[n] = Vi1_bis(punto[0],st.session_state.v,'interior',OBS)
            Va_bis1v[n] = Va1_bis(punto[0],st.session_state.v,'exterior',OBS)
            Vi2v[n] = Vi2(punto[0],OBS)
            Va2v[n] = Va2(punto[0],OBS)
            Vi_bis2v[n] = Vi2_bis(punto[0],OBS)
            Va_bis2v[n] = Va2_bis(punto[0],OBS)
            Vi3v[n] = Vi3(punto[0], bPT, st.session_state.v, 'interior', OBS)
            Va3v[n] = Va3(punto[0], bPT, st.session_state.v, 'exterior', OBS)
            Vi_bis3v[n] = Vi3_bis(punto[0], bPT, st.session_state.v, 'interior', OBS)
            Va_bis3v[n] = Va3_bis(punto[0], bPT, st.session_state.v, 'exterior', OBS)
            Vi4v[n] = Vi4(punto[0],OBS)
            Va4v[n] = Va4(punto[0],OBS)
            Vi_bis4v[n] = Vi4_bis(punto[0],OBS)
            Va_bis4v[n] = Va4_bis(punto[0],OBS)
            alphaosci[n] = alpha_osc(punto[0],'interior')*180/pi
            alphaosca[n] = alpha_osc(punto[0],'exterior')+180/pi
            tnv[n] = TN(punto[0],OBS)
            kv[n] = K(punto[0])
            n += 1
    vf = pd.DataFrame({'Si(m)':Siv, 'Sa(m)':Sav, 'qSDi(m)':qSDiv, 'qSDa(m)':qSDav, 'qSIi(m)':qSIiv, 'qSIa(m)':qSIav, 'j1i(m)':j1iv, 'j1a(m)':j1av,
    'j1*i(m)':j1i_bisv, 'j1*a(m)':j1a_bisv, 'j2i(m)':j2iv, 'j2a(m)':j2av, 'j2*i(m)':j2i_bisv, 'j2*a(m)':j2a_bisv,
    'j3i(m)':j3iv, 'j3a(m)':j3av, 'j3*i(m)':j3i_bisv, 'j3*a(m)':j3a_bisv, 'j4i(m)':j4iv, 'j4a(m)':j4av, 'j4*i(m)':j4i_bisv, 'j4*a(m)':j4a_bisv,
    'Vi1(m)':Vi1v, 'Va1(m)':Va1v, 'Vi1*(m)':Vi_bis1v, 'Va1*(m)':Va_bis1v, 'Vi2(m)':Vi2v, 'Va2(m)':Va2v, 'Vi2*(m)':Vi_bis2v, 'Va2*(m)':Va_bis2v,
    'Vi3(m)':Vi3v, 'Va3(m)':Va3v, 'Vi3*(m)':Vi_bis3v, 'Va3*(m)':Va_bis3v, 'Vi4(m)':Vi4v, 'Va4(m)':Va4v, 'Vi4*(m)':Vi_bis4v, 'Va4*(m)':Va_bis4v,
    'Alpha_osc i(º)':alphaosci, 'Alpha_osc a (º)':alphaosca, 'TN(m)':tnv, 'K':kv})
    return vf


#Obtener gálibo
galibo_limite = gal_limite(puntos)[7]
galibo_nominal = gal_nominal(puntos)[7]
variables_unicas = obtener_variables_unicas(st.session_state.v,OBS)
variables_contorno = obtener_variables_contorno(puntos)

st.session_state.var = variables_unicas
st.session_state.input = obtener_inputs()

#st.write(galibo_limite)

#Generación figuras
import shapely
from shapely.geometry import Polygon
import matplotlib.pyplot as plt

##Defeinir poligonos como lista de puntos
gal1 = galibo_limite[galibo_limite.columns[0:2]]
gal2 = galibo_limite[galibo_limite.columns[2:4]]
gal3 = galibo_limite[galibo_limite.columns[4:6]]
gal4 = galibo_limite[galibo_limite.columns[6:8]]
#st.write(gal1)
#st.write(gal2)
#st.write(gal3)
#gal1 = [list(row) for row in galibo_limite.values] prova que no funciona

gn1 = galibo_nominal[galibo_nominal.columns[0:2]]
gn2 = galibo_nominal[galibo_nominal.columns[2:4]]
gn3 = galibo_nominal[galibo_nominal.columns[4:6]]
gn4 = galibo_nominal[galibo_nominal.columns[6:8]]

##Crear poligonos
pol1 = Polygon(gal1)
pol2 = Polygon(gal2)
pol3 = Polygon(gal3)
pol4 = Polygon(gal4)

pn1 = Polygon(gn1)
pn2 = Polygon(gn2)
pn3 = Polygon(gn3)
pn4 = Polygon(gn4)

##Dibujar poligonos individuales
fig, ax = plt.subplots()
ax.plot(*pol1.exterior.xy)
ax.plot(*pol2.exterior.xy)
ax.plot(*pol3.exterior.xy)
ax.plot(*pol4.exterior.xy)
#plt.show()

#st.pyplot(fig)

gal_lim_unified = pol1.union(pol2).union(pol3).union(pol4)

gal_nom_unified = pn1.union(pn2).union(pn3).union(pn4)

galibo_limite_pol, coords_lim, offsets = shapely.to_ragged_array([gal_lim_unified])

galibo_nominal_pol, coords_nom, offsets = shapely.to_ragged_array([gal_nom_unified])

gal_lim = pd.DataFrame(coords_lim, columns = ['Gálibo límite (b)', 'Gálibo límite (h)'])

gal_nom = pd.DataFrame(coords_nom, columns = ['Gálibo nominal(b)', 'Gálibo nominal (h)'])

#st.table(gal_lim)

#st.write(gal_nom)


if st.button("Gálibo límite"):
    ##Dibujar poligonos individuales
    plt.figure(figsize=(5,8))
    fig_part, ax = plt.subplots()
    fig1, = ax.plot(*pol1.exterior.xy)
    fig2, = ax.plot(*pol2.exterior.xy)
    fig3, = ax.plot(*pol3.exterior.xy)
    fig4, = ax.plot(*pol4.exterior.xy)
    ax.set_xlim(-2.5,2.5)
    ax.set_ylim(-0.25,5.)
    ax.set_aspect('equal', adjustable='box', anchor='C')
    plt.grid(True, linestyle = '--')
    plt.xlabel('Ancho (m)')
    plt.ylabel('Altura (m)')
    ax.legend([fig1, fig2, fig3, fig4], ['Ancho máximo con altura compatible (vmax)', 'Ancho máximo con altura compatible (v=0)',
    'Altura máxima con ancho compatible (vmax)', 'Altura máxima con ancho compatible (v=0)'], bbox_to_anchor=(1., 1.28), loc=1)
    #st.pyplot(fig)
    plt.savefig('Casos particulares gálibo límite.png', bbox_inches='tight')


    plt.figure(figsize=(5,5), tight_layout = True)
    fig_gal, ax = plt.subplots()
    ax.plot(*gal_lim_unified.exterior.xy)
    ax.set_xlim(-2.5,2.5)
    ax.set_ylim(-0.25,5.)
    ax.set_aspect('equal', adjustable='box', anchor='C')
    plt.grid(True, linestyle = '--')
    plt.xlabel('Ancho (m)')
    plt.ylabel('Altura (m)')
    plt.suptitle('Gálibo límite de implantación de obstáculos')
    plt.title('%s + %s'%(st.session_state.partes_altas, st.session_state.partes_bajas))

    #st.pyplot(fig)
    plt.savefig('Gálibo límite.png')

    col5, col6 = st.columns(2)

    with col5:
        st.markdown('**Gálibos casos particulares**')
        st.pyplot(fig_part)

    with col6:
        st.markdown('**Gálibo límite de implantación de obstáculos**')
        st.pyplot(fig_gal)

    #st.write(gal_lim)
    with pd.ExcelWriter('Gálibo límite.xlsx') as writer:
        galibo_limite.to_excel(writer, sheet_name='Casos particulares')
        gal_lim.to_excel(writer, sheet_name='Gálibo límite')
        variables_unicas.to_excel(writer, sheet_name='Variables únicas')
        variables_contorno.to_excel(writer, sheet_name='Variables contorno')
    #galibo_limite.to_excel('Gálibo límite.xlsx')

if st.button("Gálibo nominal"):
    ##Dibujar poligonos individuales
    plt.figure(figsize=(5,8))
    fig, ax = plt.subplots()
    fig1, = ax.plot(*pn1.exterior.xy)
    fig2, = ax.plot(*pn2.exterior.xy)
    fig3, = ax.plot(*pn3.exterior.xy)
    fig4, = ax.plot(*pn4.exterior.xy)
    ax.set_xlim(-2.5,2.5)
    ax.set_ylim(-0.25,5.)
    ax.set_aspect('equal', adjustable='box', anchor='C')
    plt.grid(True, linestyle = '--')
    plt.xlabel('Ancho (m)')
    plt.ylabel('Altura (m)')
    ax.legend([fig1, fig2, fig3, fig4], ['Ancho máximo con altura compatible (vmax)', 'Ancho máximo con altura compatible (v=0)',
    'Altura máxima con ancho compatible (vmax)', 'Altura máxima con ancho compatible (v=0)'], bbox_to_anchor=(1., 1.28), loc=1)
    st.pyplot(fig)
    plt.savefig('Casos particulares gálibo nominal.png', bbox_inches='tight')

    plt.figure(figsize=(5,5), tight_layout = True)
    fig, ax = plt.subplots()
    ax.plot(*gal_nom_unified.exterior.xy)
    ax.set_xlim(-2.5,2.5)
    ax.set_ylim(-0.25,5.)
    ax.set_aspect('equal', adjustable='box', anchor='C')
    plt.grid(True, linestyle = '--')
    plt.xlabel('Ancho (m)')
    plt.ylabel('Altura (m)')
    plt.suptitle('Gálibo nominal de implantación de obstáculos')
    plt.title('%s + %s'%(st.session_state.partes_altas, st.session_state.partes_bajas))

    st.pyplot(fig)
    plt.savefig('Gálibo nominal.png')


    #st.write (gal_nom)
    with pd.ExcelWriter('Gálibo nominal.xlsx') as writer:
        galibo_nominal.to_excel(writer, sheet_name='Casos particulares')
        gal_nom.to_excel(writer, sheet_name='Gálibo nominal')
        variables_unicas.to_excel(writer, sheet_name='Variables únicas')
        variables_contorno.to_excel(writer, sheet_name='Variables contorno')
    #galibo_nominal.to_excel('Gálibo nominal.xlsx')