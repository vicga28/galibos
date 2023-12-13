import docx
import streamlit as st
import pandas as pd
import numpy as np
from math import pi
from PIL import Image

st.set_page_config(
    page_title = 'Calculadora de gálibos',
    page_icon = '🚊',
    layout = 'centered'
)

st.markdown ("# Fórmulas")

st.write('Aquí se mostrarán todas las fórmulas utilizadas para el cálculo de los gálibos ferroviarios.')

st.markdown('''Ampliaciones a considerar:
- Salientes
- Desplazamientos cuasiestáticos laterales
- Desplazamientos aleatorios laterales
- Márgenes complementarios''')

st.subheader('Salientes', divider = 'grey')

st.subheader('Desplazamientos cuasiestáticos laterales', divider = 'grey')
st.latex(r'''
    qs_{Di} = qs_{Da} = (\frac{s_{0}}{L}) · (D - D_{0})_{>0} · (h - h_{c0})_{>0}
    ''')

st.latex(r'''
    qs_{Ii} = qs_{Ia} = (\frac{s_{0}}{L}) · (I - I_{0})_{>0} · (h - h_{c0})_{>0}
    ''')

st.subheader('Distancie entreejes', divider = 'grey')
image = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/entreeje.jpg')
st.image(image, caption = 'Distancia nominal entre ejes de vías (valores normales)')