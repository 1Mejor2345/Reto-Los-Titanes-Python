##LIMPIEZA Y FILTRADO DE DATOS

import openpyxl
from openpyxl.utils import column_index_from_string
from openpyxl.comments import Comment

#Cargamos el archivo de excel
libro = openpyxl.load_workbook("PYWEEKEND.xlsx")
hoja = libro.active

#Convertimos los comentarios a valores en las celdas respectivas
fila_comentario = 4 #Esta es la fila con las características como comentarios
min_columna = column_index_from_string("G") #Es la columnna desde donde empiezan los comentarios a trasformar
max_columna = column_index_from_string("DE")

for fila in hoja.iter_rows(min_col=min_columna, max_col=max_columna, min_row=fila_comentario, max_row=fila_comentario):
    for celda in fila:
        if celda.comment:
            celda.value = celda.comment.text.replace("HP:", "").replace("HP", "").replace("Alienware:", "").strip().upper()
	    #Este for itera por cada celda para asignarle como valor su comentario limpio respectivo

#Guardamos en un nuevo excel (checkpoint 1)
libro.save("PYWEEKEND_COMENTARIOS.xlsx")
print("Archivo PYWEEKEND_COMENTARIOS.xlsx creado correctamente :)")

#Llenamos las celdas Undefined
import pandas as pd
import numpy as np

#Creamos un dataframe para poder llenar las celdas con valores vacíos, y creamos un MultiIndex para manejarnos mejor
df = pd.read_excel("PYWEEKEND_COMENTARIOS.xlsx", header=[0,1,2,3], index_col=[2,3])
df.index.names = ["Procedencia", "Nro. paquete"]
df.columns.names = ["Análisis", "Subanálisis", "Sub-subanálisis", "Final"]

#Ignoramos metadatos (Nro, Sitio, Corte, Depósito)
df = df.iloc[:, 4:]

#Reemplazaremos valores de celdas vacías por un nuevo Sub-subanálisis
#Conseguimos en forma de listas los valores que están en cada columna
nivel0 = df.columns.get_level_values(0)
nivel1 = df.columns.get_level_values(1)
nivel2 = df.columns.get_level_values(2)
nivel3 = df.columns.get_level_values(3)

#En este nuevo nivel reemplazamos las celdas vacías que al transformar a Dataframe contienen "Unnamed"
nuevo_nivel1 = ["Partes / Forma de la Vasija" if "Unnamed" in str(val) else val for val in nivel1]

df.columns = pd.MultiIndex.from_arrays([nivel0, nuevo_nivel1, nivel2, nivel3], names = df.columns.names)

#Filtramos las columnas que tengan en el tercer nivel Totales y valores vacíos
mask = ~df.columns.get_level_values(3).isin(["Total", "N/A"])
df = df.loc[:, mask]

#Agrupamos en suma en caso de que se repitan unidades arqueológicas (Se repitió una)
df = df.groupby(level=[0,1]).sum()

#Guardamos como excel filtrado (checkpoint 2)
df.to_excel("PYWEEKEND_FILTRADO.xlsx")
print("Archivo PYWEEKEND_FILTRADO.xlsx creado correctamente :)")

##ESTRUCTURACIÓN DE LOS DATOS

#Creamos una función que transforma las filas en diccionarios anidados
def fila_a_diccionario(fila, columnas): 
    resultado = {}
    for col in columnas:
        valor = fila[col]
        if pd.api.types.is_number(valor) and not pd.isna(valor) and valor > 0: #Verificamos que sea un número mayor a cero y que no sea una celda vacía
            nivel1, nivel2, nivel3, nivel4 = col
            if nivel1 not in resultado:
                resultado[nivel1] = {}
            if nivel2 not in resultado[nivel1]:
                resultado[nivel1][nivel2] = {}
            if nivel3 not in resultado[nivel1][nivel2]:
                resultado[nivel1][nivel2][nivel3] = {}
            resultado[nivel1][nivel2][nivel3][nivel4] = valor
    return resultado

#Creamos una función para transforma un dataframe a un diccionario anidado ayudandonos de la función anterior
def df_a_diccionario(df):
    resultado = {}
    for idx_fila, fila in df.iterrows(): #iterrows es una función que me devuelve los índices de cada fila junto con una serie de esa fila
        procedencia, paquete = idx_fila
        if procedencia not in resultado:
            resultado[procedencia] = {}
        resultado[procedencia][paquete] = fila_a_diccionario(fila, df.columns)
    return resultado

#Creamos el archivo de texto formato JSON a partir del dataframe
import json
resultado_json = df_a_diccionario(df)
with open("resultado.json", "w", encoding="utf-8") as f:
    json.dump(resultado_json, f, indent=2, ensure_ascii=False)
print("Archivo resultado.json creado correctamente :)")