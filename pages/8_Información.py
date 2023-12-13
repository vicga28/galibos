import docx
import streamlit as st
import pandas as pd
import numpy as np
from math import pi

st.set_page_config(
    page_title = 'Calculadora de gálibos',
    page_icon = '🚊',
    layout = 'centered'
)

st.markdown ("# Información")

st.write('La presente página sirve como recurso para el cálculo de los gálibos ferroviarios según la *Orden FOM/1630/2015, de 14 de julio, por el que se aprueba la "Instrucción Ferroviaria de Gálibos"*.')
st.write('Según la norma EN 15273-3:2013, el **gálibo de implantación de obstáculos** es eñ espacio en torno a la vía que no debe ser invadido por obstáculos, ni por vehículos que circulen por las vías adyacentes, al objeto de preservar la seguridad en la explotación.')
st.write('''Se consideran 3 tipos de gálibo de implantación de obstáculos:
- Gálibo límite
- Gálibo nominal
- Gálibo uniforme''')
st.markdown('**Gálibo límite**')
st.write('''Se define para un punto o tramo de línea. Delimita el espacio que no debe invadir ningún obstáculo en circustancia alguna
a fin de permitir la circulación normal de los vehículos, más una reserva para considerar las variaciones tolerables de la posición de la vía que se producen entre dos operaciones normales de mantenimiento.
Este gálibo se utilliza, por ejemplo, para comprobar si es posible el paso de transportes excepcionales por un determinado punto.''')
st.markdown('**Gálibo nominal**')
st.write('''Se define para un punto o tramo de línea. Es similar al gálibo límite, pero incorporando unos márgenes complementarios para la circulación de transportes excepcionales, incrementos de velocidad, etc.''')
st.markdown('**Gálibo uniforme**')
st.write('''Se define para una línea. Es un gálibo nominal obtenido para una envolvente de parámetros (radios, peraltes, etc.) suficientemente desfavorables, que no se superan en la mayor parte de la línea. De esta forma se puede utilizar un único gálibo para toda ella, comprobando que no se superan los parámetros de partida.''')