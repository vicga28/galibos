import streamlit as st
import pandas as pd
import numpy as np
from math import pi

st.set_page_config(
    page_title = 'Calculadora de gálibos',
    page_icon = '🚊',
    layout = 'centered'
)

st.markdown ("# Gálibo pantógrafo")
#st.sidebar.markdown(" # Gálibo pantógrafo")

#GÁLIBO DEL PANTÓGRAFO

ancho_mesilla_existente = [1.700, 1.950, 1.600]
corriente_existente = ['cc', 'ca']
tension_catenaria_existente = [1.5, 3.0, 25] #en kV

tipo_catenaria_existente = ['rigida', 'elastica']
catenaria_existente = ['CA-160', 'CAU-220', 'CA-220', 'SICAT H 1.0', 'EAC-350']

tipo_catenaria = st.selectbox("Tipo de catenaria:", ["Elástica", "Rígida"])
ancho_mesilla = st.number_input("Ancho de la mesilla (m):", format='%3.f')
corriente = st.selectbox("Tipo de corriente:", ["Corriente contínua (c.c.)", "Corriente alterna (c.a.)"])


if tipo_catenaria == "Elástica":
    tipo_catenaria = "elastica"
elif tipo_catenaria == "Rígida":
    tipo_catenaria = "rigida"

if corriente == "Corriente contínua (c.c.)":
    corriente = "cc"
elif corriente == "Corriente alterna (c.a.)":
    corriente = "ca"

tipo_catenaria = 'elastica'
catenaria = 'EAC-350'

ancho_mesilla = 1.950
corriente = 'ca'
tension_catenaria = 25

cw = 0

#Altura de la articulación más baja del pantógrafo respecto al plano de rodadura
ht = 5.000
#Altura máxima de verificación del gálibo
h0_bis = 6.500
#Altura del centro de balanceo del vehículo, medida sobre el plano de rodadura y perpendicular a éste
hc = 5.150

#Ancho pantografo
bp = 1.950

hf = 5.300

##Factor de seguridad para la determinación del gálibo mecánico del pantógrafo
K_bis = 1

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

def bw():
    if corriente == 'cc':
        if tension_catenaria == 1.5:
            bw = 0.850
        elif tension_catenaria == 3.0:
            bw = 0.975
        else:
            print('No corresponde con las opciones disponibles.')
        if ancho_mesilla == 1.700:
            bw = 0.850
        elif ancho_mesilla == 1.950:
            bw = 0.975
        else:
            print('No corresponde con las opciones disponibles.')
    elif corriente == 'ca':
        if tension_catenaria == 25:
            if ancho_mesilla == 1.950:
                bw = 0.975
            elif ancho_mesilla == 1.600:
                bw = 0.800
            else:
                print('No corresponde con las opciones disponibles.')
        else:
            print('No corresponde con las opciones disponibles.')
    else:
        print('No corresponde con las opciones disponibles.')
    return bw

def ep(h):
    #z1 = 
    #Para la altura de verificación máx (h'0)
    #ep0_bis = 0.0375 + (z1 + ((0.03*(h-ht)/(h0_bis - ht))**2+0.01**2+(0.005*(h - hc))**2)) - 0.005
    #ep0 = ep0_bis + 0.02
    #Para la altura de verificación mín (h'u)
    #epu_bis =
    #epu = epu_bis
    if st.session_state.partes_altas == 'GEE10' or st.session_state.partes_altas == 'GED10':
        ep0 = 0.150
        epu = 0.082
        ep = (51*h/900-97/600)
    elif st.session_state.partes_altas == 'GEC16' or st.session_state.partes_altas == 'GEB16' or st.session_state.partes_altas == 'GEC16':
        ep0 = 0.170
        epu = 0.110
        ep = 0.04*h-0.09
    elif st.session_state.partes_altas == 'GA' or st.session_state.partes_altas == 'GB' or st.session_state.partes_altas == 'GC':
        ep0 = 0.170
        epu = 0.110
        ep = 0.04*h-0.09
    else:
        ep = 0
    return ep

def alpha_osc_p(x):
    if st.session_state.tipo_via == 'balasto':
        if st.session_state.ancho_via == 1.000:
            if x.lower() == 'interior':
                alpha_osc_p = 0.11
            elif x.lower() == 'exterior':
                alpha_osc_p = 0.60
        else:
            if st.session_state.estado_via == 'bueno':
                if x.lower() == 'interior':
                    alpha_osc_p = 0.06
                elif x.lower() == 'exterior':
                    alpha_osc_p = 0.34
            elif st.session_state.estado_via  == 'malo':
                if x.lower() == 'interior':
                    alpha_osc_p = 0.11
                elif x.lower() == 'exterior':
                    alpha_osc_p = 0.6
    elif st.session_state.tipo_via == 'placa':
        if x.lower() == 'interior':
            alpha_osc_p = 0.06
        elif x.lower() == 'exterior':
            alpha_osc_p = 0.34
    alpha_osc_p = alpha_osc_p * pi /180
    return alpha_osc_p

def Si_a_bis(r):
    if st.session_state.partes_altas == 'GEE10' or st.session_state.partes_altas == 'GED10':
        Si_bis = 1 / r + (1.030 - 0.970) / 2
        Sa_bis = Si_bis
    elif st.session_state.partes_altas == 'GEC16' or st.session_state.partes_altas == 'GEB16' or st.session_state.partes_altas == 'GEA16':
        Si_bis = 2.5/r + (1.698-1.643)/2
        Sa_bis = Si_bis
    elif st.session_state.partes_altas == 'GA' or st.session_state.partes_altas == 'GB' or st.session_state.partes_altas == 'GC':
        Si_bis = 2.5/r + (1.465-1.410)/2
        Sa_bis = Si_bis
    return Si_bis, Sa_bis

def qsi_a_bis(h, D, I):
    if st.session_state.partes_altas == 'GEE10' or st.session_state.partes_altas == 'GED10':
        L = 1.055
        s0_bis = 0.225
        hc0_bis = 0.5
        D0_bis = 0.07
        I0_bis = 0.07
        d = 0.970
    elif st.session_state.partes_altas == 'GA' or st.session_state.partes_altas == 'GB' or st.session_state.partes_altas == 'GC':
        L = 1.500
        s0_bis = 0.225
        hc0_bis = 0.5
        D0_bis = 0.066
        I0_bis = 0.066
        d = 1.140
    elif st.session_state.partes_altas == 'GEA16' or st.session_state.partes_altas == 'GEB16' or st.session_state.partes_altas == 'GEC16' or st.session_state.partes_altas == 'GHE16':
        L = 1.733
        s0_bis = 0.225
        hc0_bis = 0.5
        D0_bis = 0.066
        I0_bis = 0.066
        d = 1.643
    if D > D0_bis:
        qsi_bis = s0_bis / L * (D - D0_bis) * (h - hc0_bis)
    else:
        qsi_bis = 0
    if I > I0_bis:
        qsa_bis = s0_bis / L * (I - I0_bis) * (h - hc0_bis)
    else: qsa_bis = 0
    return qsi_bis, qsa_bis

def heff(hf):
    if tipo_catenaria == 'rigida':
        fs_vmax = 0.015
        fs_v0 =  0.015
        fw = 0.070
    else:
        fw = 0.070
    if catenaria == 'CA-160':
        fs_vmax = 0.195
        fs_v0 = 0.078
    elif catenaria == 'CAU-220':
        fs_vmax = 0.152
        fs_v0 = 0.046
    elif catenaria == 'CA-220':
        fs_vmax = 0.148
        fs_v0 = 0.045
    elif catenaria == 'SICAT H 1.0':
        fs_vmax = 0.154
        fs_v0 = 0.040
    elif catenaria == 'EAC-350':
        fs_vmax = 0.162
        fs_v0 = 0.041
    else:
        print('No está considerada la catenaria indicada.')
    heff_vmax = hf + fs_vmax + fw
    heff_v0 = hf + fs_v0 + fw
    return heff_vmax, heff_v0

def belec():
    if corriente == 'cc':
        if tension_catenaria == 1.5:
            belec_vmax = 0.050
            belec_v0 = 0.100
        elif tension_catenaria == 3.0:
            belec_vmax = 0.050
            belec_v0 = 0.150
        else:
            print('No corresponde con las opciones disponibles.')
    elif corriente == 'ca':
        if tension_catenaria == 25:
            belec_vmax = 0.150
            belec_v0 = 0.270
        else:
            print('No corresponde con las opciones disponibles.')
    else:
        print('No corresponde con las opciones disponibles.')
    return belec_vmax, belec_v0

def j_bis(h,vmax, ext):
    if st.session_state.partes_altas == 'GED10' or st.session_state.partes_altas == 'GEE10':
        L = 1.055
    elif st.session_state.partes_altas == 'GA' or st.session_state.partes_altas == 'GB' or st.session_state.partes_altas == 'GC':
        L = 1.500
    elif st.session_state.partes_altas == 'GEA16' or st.session_state.partes_altas == 'GEB16' or st.session_state.partes_altas == 'GEC16' or st.session_state.partes_altas == 'GHE16':
        L = 1.733
    if h > 0.5:
        j_bis = K_bis*(Tvia()**2+(h+0.225*(h-0.5))**2*(TD(vmax)/L)**2+(np.tan(alpha_susp)**2+np.tan(alpha_c)**2+np.tan(alpha_osc_p(ext))**2)*(h-0.5)**2)**0.5
    else:
        j_bis = K_bis*(Tvia()**2+h**2*(TD(vmax)/L)**2)**0.5
    return j_bis

def bobsi_a(h,D,I,r,vmax):
    bobs_i = bw() + ep(h) + Si_a_bis(r)[0] + qsi_a_bis(h,D,I)[0] + j_bis(h,vmax,'interior')
    bobs_a = bw() + ep(h) + Si_a_bis(r)[1] + qsi_a_bis(h,D,I)[1] + j_bis(h,vmax,'exterior')
    return bobs_i, bobs_a
                 
def bobsi_a_e(h,D,I,r,v):
    #Lado interior de la curva
    bobsi_e_i = bobsi_a(h,D,I,r,v)[0] + belec()[1] - cw
    #Lado exterior de la curva
    bobsa_e_a= bobsi_a(h,D,I,r,v)[1] + belec()[0] - cw
    return bobsi_e_i, bobsa_e_a

def heff_e(hf):
    heff_e_vmax = heff(hf)[0] + belec()[0]
    heff_e_v0 = heff(hf)[1] + belec()[1]
    return heff_e_vmax,heff_e_v0

def pantografo():
    p0 = [bp, h0_bis]
    p1 = [bp, ht]
    puntos = [p0, p1]
    return puntos

def galibo_mecanico_pantografo(contorno):
    #Velocidad maxima
    ##Punto superior
    ###Lado interior curva
    bi0 = bobsi_a(contorno[0][1],st.session_state.d,st.session_state.i,st.session_state.r,st.session_state.v)[0]
    h_vmax = heff(hf)[0]
    ###Lado exterior curva
    ba0 = bobsi_a(contorno[0][1],st.session_state.d,st.session_state.i,st.session_state.r,st.session_state.v)[1]
    ##Punto inferior
    ###Lado interior curva
    bit = bobsi_a(contorno[1][1],st.session_state.d,st.session_state.i,st.session_state.r,st.session_state.v)[0]
    ###Lado exterior curva
    bat = bobsi_a(contorno[1][1],st.session_state.d,st.session_state.i,st.session_state.r,st.session_state.v)[1]
    #Parado (velocidad = 0)
    h_v0 = heff(hf)[1]
    #Contorno velocidad maxima
    dm = pd.DataFrame({'Gálibo mecánico (b)': [bi0, bit, -bat, -ba0],
                   'Gálibo mecánico (h)': [h_v0, h_vmax, h_vmax, h_v0]})
    return dm

def galibo_electrico_pantografo(contorno):
    #Velocidad maxima
    ##Punto superior
    ###Lado interior curva
    bi0 = bobsi_a_e(contorno[0][1],st.session_state.d,st.session_state.i,st.session_state.r,st.session_state.v)[0]
    h_vmax = heff_e(hf)[0]
    ###Lado exterior curva
    ba0 = bobsi_a_e(contorno[0][1],st.session_state.d,st.session_state.i,st.session_state.r,st.session_state.v)[1]
    ##Punto inferior
    ###Lado interior curva
    bit = bobsi_a_e(contorno[1][1],st.session_state.d,st.session_state.i,st.session_state.r,st.session_state.v)[0]
    ###Lado exterior curva
    bat = bobsi_a_e(contorno[1][1],st.session_state.d,st.session_state.i,st.session_state.r,st.session_state.v)[1]
    #Parado (velocidad = 0)
    h_v0 = heff_e(hf)[1]
    #Contorno velocidad maxima
    de = pd.DataFrame({'Gálibo eléctrico (b)': [bi0, bit, -bat, -ba0],
                   'Gálibo eléctrico (h)': [h_v0, h_vmax, h_vmax, h_v0]})
    return de





galibo_mecanico = galibo_mecanico_pantografo(pantografo())
galibo_electrico = galibo_electrico_pantografo(pantografo())
dc = galibo_mecanico.join(galibo_electrico)

if st.button("Gálibo mecánico:"):
    galibo_mecanico.to_excel("Gálibo mecánico.xlsx")

if st.button("Gálibo eléctrico:"):
    galibo_electrico.to_excel("Gálibo eléctrico.xlsx")

if st.button("Gálibo pantógrafo:"):
    dc.to_excel("Gálibo pantógrafo.xlsx")


