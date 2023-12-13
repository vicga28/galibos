import streamlit as st
import pandas as pd
import numpy as np
from math import pi

st.set_page_config(
    page_title = 'Calculadora de gálibos',
    page_icon = '🚊',
    layout = 'centered'
)

st.markdown ("# Distancia vía-andén")
#st.sidebar.markdown(" # Distancia vía-andén")

#INPUTS

##Altura borde andén (respecto el plano de rodadura y perpendicular a éste)
hq = st.number_input("Altura borde andén (respecto el plano de rodadura y perpendicular a éste) (m):",format='%.3f')

##Tipo de andén (0: Con bordillo retranqueado / 1: Vertical recto)

tipo_anden = st.selectbox("Tipo de andén:", ["Con bordillo retranqueado", "Vertical recto"])

if tipo_anden == "Con bordillo retranqueado":
    tipo_anden = 0
elif tipo_anden == "Vertical recto":
    tipo_anden = 1

#Definición funciones cálculos
def k(h):
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

##Factor de seguridad para la determinación del gálibo límite de implantación de obstáculos
#Controlar desplazamientos aleatorios laterales
def K(h):
    if h < 0.5:
        K = 1
    else:
        K = 1.2
    return K

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


###Nomenclatura

### dqa
### hnez: Altura del bordillo del borde de andén
### hq: Altura del borde de andén, medida sobre el plano de rodadura y perpendicular a éste
### hminCR: Altura de la esquina inferior del contorno de referencia

### bCR: Semiancho del contorno de referencia

def dqa(tipo_anden, h,d):
    if tipo_anden == 0:
        hnez = h
        dqa = d / st.session_state.L * hnez
    elif tipo_anden == 1:
        hq = h
        dqa = d / st.session_state.L * (hq - st.session_state.hminCR)
    return dqa

def bqi_a(h,R,d,v, tipo_anden):
    bqi = st.session_state.bCR + Si_a(h,R)[0] + qSDi_a(h,d)[0] + j1(h,st.session_state.v,'interior')
    bqa = st.session_state.bCR + Si_a(h,R)[1] + qSDi_a(h,d)[1] + j1(h,st.session_state.v,'exterior') + dqa(tipo_anden,h,d)
    return bqi,bqa

ancho_anden = bqi_a(hq,st.session_state.r,st.session_state.d,st.session_state.v,tipo_anden)

st.write("El espacio necesario entre la vía y el andén debe ser como mínimo %s m en el lado interior y %s m en el lado exterior." % (ancho_anden[0].round(2), ancho_anden[1].round(2)))