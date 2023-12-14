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

st.markdown ("# Contornos de referencia")

#image_path = Path("C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/").with_name("GEA16.png").relative_to(Path.cwd())
#st.image(str(image_path))

st. subheader('Ancho ibérico (1.668 mm)', divider = 'grey')
col1, col2, col3 = st.columns(3)

with col1:
    st.image('https://github.com/vicga28/galibos/blob/main/calculo_galibos/GEA16.jpg?raw=true',
             caption = 'Contorno de referencia del gálibo cinemático GEA16. Partes altas')
    image = Image.open('https://github.com/vicga28/galibos/blob/main/calculo_galibos/GEA16.jpg?raw=true')
    st.image(image, caption = 'Contorno de referencia del gálibo cinemático GEA16. Partes altas')
    image2 = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GEI1.jpg')
    st.image(image2, caption = 'Contorno de referencia del gálibo cinemático GEI1. Partes bajas')

with col2:
    image = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GEB16.jpg')
    st.image(image, caption = 'Contorno de referencia del gálibo cinemático GEB16. Partes altas')
    mage2 = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GEI2.jpg')
    st.image(image2, caption = 'Contorno de referencia del gálibo cinemático GEI2. Partes bajas')

with col3:
    image = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GEC16.jpg')
    st.image(image, caption = 'Contorno de referencia del gálibo cinemático GEC16. Partes altas')
    mage2 = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GEI3.jpg')
    st.image(image2, caption = 'Contorno de referencia del gálibo cinemático GEI3. Partes bajas')

st.subheader('Ancho europeo (1.435 mm)', divider = 'gray')
col1, col2, col3 = st.columns(3)

with col1:
    image = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/G.jpg')
    st.image(image, caption = 'Contorno de referencia de los gálibos cinemáticos GA, GB y GC. Partes altas')
    image2 = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GI1.jpg')
    st.image(image2, caption = 'Contorno de referencia del gálibo cinemático GI1. Partes bajas')

with col2:
    image2 = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GI2.jpg')
    st.image(image2, caption = 'Contorno de referencia del gálibo cinemático GI2. Partes bajas')

with col3:
    image2 = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GI3.jpg')
    st.image(image2, caption = 'Contorno de referencia del gálibo cinemático GI3. Partes bajas')

st.subheader('Ancho métrico (1.000 mm)', divider = 'gray')
col1, col2, col3 = st.columns(3)

with col1:
    image = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GEE10.jpg')
    st.image(image, caption = 'Contorno de referencia del gálibo cinemático GEE10. Partes altas')

with col2:
    image2 = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GED10.jpg')
    st.image(image2, caption = 'Contorno de referencia del gálibo cinemático GED10. Partes altas')

with col3:
    image2 = Image.open('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GEE10_i.jpg')
    st.image(image2, caption = 'Contorno de referencia del gálibo cinemático GEE10. Partes bajas')

#st.image('C:/Users/gullonav/Desktop/Gálibos/calculo_galibos/GEA16.jpg')

#st.image('GEA16.jpg', caption = 'Contorno de referencia del gálibo cinemático GEA16. Partes altas')
