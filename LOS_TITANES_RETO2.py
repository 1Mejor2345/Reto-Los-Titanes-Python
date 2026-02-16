import LOS_TITANES_RETO1
import matplotlib.pyplot as plt
import json
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter

# ---------------------------------------------------------
# 1. CARGA DE DATOS
# ---------------------------------------------------------
with open("resultado.json", "r", encoding="utf-8") as f:
    data = json.load(f)

tecnica_exterior = {}
tecnica_interior = {}
tecnica_manufactura = {}
colores_exterior = {}
colores_interior = {}
colores_engobe = {}

print("Estas son las procedencias disponibles: ")
for elemento_procedencia in set(data.keys()):
    print(f" - {elemento_procedencia}")
procedencia_input = input(f"Escoga una procedencia de un hallazgo arqueológico: ").strip().upper()

for procedencia, procedencia_section in data.items():
    if procedencia == procedencia_input:
        print(f"Estas son las Nro. de paquetes disponibles de la procedencia {procedencia}")
        for elemento_paquete in procedencia_section.keys():
            print(f"- {elemento_paquete}")
        paquete_input = input(f"Escoga un Nro. de paquete: ").strip().upper()

# Procesamiento de datos del JSON
for procedencia, procedencia_section in data.items():
    if procedencia == procedencia_input:
        for paquete, paquete_section in procedencia_section.items():  
            if paquete == paquete_input:
                for analisis, analisis_section in paquete_section.items():
                    if analisis == "Análisis morfológico" and "Borde" in analisis_section:
                        borde_section = analisis_section["Borde"]
                        if "Técnica de manufactura" in borde_section:
                            tecnica_de_manufactura_section = borde_section["Técnica de manufactura"]
                            for tecnica, num_tecnica in tecnica_de_manufactura_section.items():
                                if tecnica not in tecnica_manufactura:
                                    tecnica_manufactura[tecnica] = 0
                                tecnica_manufactura[tecnica] += num_tecnica
                    
                    if analisis == "Análisis decorativo" and "Técnica decorativa" in analisis_section:
                        tecnicas_decorativas_section = analisis_section["Técnica decorativa"]
                        if "Exterior" in tecnicas_decorativas_section:
                            exterior_section = tecnicas_decorativas_section["Exterior"]
                            for tecnica, num_tecnica in exterior_section.items():
                                if tecnica not in tecnica_exterior:
                                    tecnica_exterior[tecnica] = 0
                                tecnica_exterior[tecnica] += num_tecnica
                        if "Interior" in tecnicas_decorativas_section:
                            interior_section = tecnicas_decorativas_section["Interior"]
                            for tecnica, num_tecnica in interior_section.items():
                                if tecnica not in tecnica_interior:
                                    tecnica_interior[tecnica] = 0
                                tecnica_interior[tecnica] += num_tecnica

                    if analisis == "Análisis tecnológico" and "Color" in analisis_section:
                        color_section = analisis_section["Color"]
                        if "Exterior" in color_section:
                            exterior_color_section = color_section["Exterior"]
                            for color, num_color in exterior_color_section.items():
                                if color not in colores_exterior:
                                    colores_exterior[color] = 0
                                colores_exterior[color] += num_color
                        if "Interior" in color_section:
                            interior_color_section = color_section["Interior"]
                            for color, num_color in interior_color_section.items():
                                if color not in colores_interior:
                                    colores_interior[color] = 0
                                colores_interior[color] += num_color
                        if "Engobe" in color_section:
                            engobe_color_section = color_section["Engobe"]
                            for color, num_color in engobe_color_section.items():
                                if color not in colores_engobe:
                                    colores_engobe[color] = 0
                                colores_engobe[color] += num_color

# Listas para gráficas
tecnicas_claves = sorted(list(set(list(tecnica_exterior.keys()) + list(tecnica_interior.keys()))))
tecnicas_exterior_valores = [tecnica_exterior.get(valor, 0) for valor in tecnicas_claves]
tecnicas_interior_valores = [tecnica_interior.get(valor, 0) for valor in tecnicas_claves]

tecnica_manufactura_clave = sorted(list(set(list(tecnica_manufactura.keys()))))
tecnica_manufactura_valores = [tecnica_manufactura.get(valor, 0) for valor in tecnica_manufactura_clave]

colores_claves = sorted(list(set(list(colores_exterior.keys())+list(colores_interior.keys())+list(colores_engobe.keys()))))
colores_interior_valores = [colores_interior.get(valor, 0) for valor in colores_claves]
colores_exterior_valores = [colores_exterior.get(valor, 0) for valor in colores_claves]
colores_engobe_valores = [colores_engobe.get(valor, 0) for valor in colores_claves]
colores_interior_exterior_valores = [(colores_interior.get(valor, 0)+colores_exterior.get(valor, 0))  for valor in colores_claves]

# ---------------------------------------------------------
# 2. GENERACIÓN DE GRÁFICOS
# ---------------------------------------------------------
plt.figure(figsize=(12,6))
barra_1 = plt.bar(tecnica_manufactura_clave, tecnica_manufactura_valores, label="Técnicas", color="orange")
plt.bar_label(barra_1, label_type="center", labels=[v if v > 0 else "" for v in tecnica_manufactura_valores]) 
plt.title(f"Frecuencia de técnica de Manufactura de la Unidad Arqueológica {procedencia_input}-{paquete_input}")
plt.xticks(rotation=60)
plt.xlabel("Técnica Manufactura")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.savefig("F_tecnica_manufactura.png")

plt.figure(figsize=(12,6))
barra_1 = plt.bar(tecnicas_claves, tecnicas_exterior_valores, label="Exterior", color="steelblue")
barra_2 = plt.bar(tecnicas_claves, tecnicas_interior_valores, label="Interior", bottom=tecnicas_exterior_valores, color="darkgreen")
plt.bar_label(barra_1, label_type="center", labels=[v if v > 0 else "" for v in tecnicas_exterior_valores]) 
plt.bar_label(barra_2, label_type="center", labels=[v if v > 0 else "" for v in tecnicas_interior_valores])
plt.title(f"Frecuencia de técnica decorativa de la Unidad Arqueológica {procedencia_input}-{paquete_input}")
plt.xticks(rotation=60)
plt.xlabel("Técnica decorativa")
plt.ylabel("Frecuencia")
plt.legend()
plt.tight_layout()
plt.savefig("F_tecnica_decorativa.png")

plt.figure(figsize=(12,6))
barra_3 = plt.bar(colores_claves, colores_interior_valores, label="Interior", color="darkgreen")
barra_4 = plt.bar(colores_claves, colores_exterior_valores, label="Exterior", color="steelblue", bottom=colores_interior_valores)
barra_5 = plt.bar(colores_claves, colores_engobe_valores, label="Engobe", color="orange",bottom=colores_interior_exterior_valores)
plt.bar_label(barra_3, label_type="center", labels=[v if v > 10 else "" for v in colores_interior_valores])
plt.bar_label(barra_4, label_type="center", labels=[v if v > 10 else "" for v in colores_exterior_valores])
plt.bar_label(barra_5, label_type="center", labels=[v if v > 10 else "" for v in colores_engobe_valores])
plt.title(f"Frecuencia de Colores de la Unidad Arqueológica {procedencia_input}-{paquete_input}")
plt.xlabel("Colores")
plt.ylabel("Frecuencia")
plt.tight_layout()
plt.legend()
plt.savefig("F_colores.png")
print("Gráficos matplot generados correctamente :)")

# -----------------------------------------------------------
# 3. INTELIGENCIA ARTIFICIAL (SETUP CORREGIDO)
# -----------------------------------------------------------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=api_key)

# MODELO 1: TEXTO (Usamos gemini-2.0-flash porque sabemos que existe en tu cuenta)
# Lo hacemos en una sola llamada para no gastar la cuota
print("Generando análisis de texto (Puede tardar 10-20 segundos)...")

prompt_completo = f"""
Actúa como un arqueólogo experto. Analiza los siguientes datos de la unidad {procedencia_input}-{paquete_input} de LLANO CHICO.

DATOS:
- Colores: {colores_claves}, {colores_interior_valores}, {colores_exterior_valores}, {colores_engobe_valores}
- Decoración: {tecnicas_claves}, {tecnicas_exterior_valores}, {tecnicas_interior_valores}
- Manufactura: {tecnica_manufactura_clave}, {tecnica_manufactura_valores}

INSTRUCCIONES:
Genera 4 párrafos separados por la palabra "SEPARADOR".
1. Análisis de patrones de colores.
2. Análisis de técnicas decorativas.
3. Análisis de manufactura.
4. Descripción visual detallada de la vasija para generar una imagen.
"""

respuesta1, respuesta2, respuesta4, descripcion = "", "", "", ""

try:
    # Usamos gemini-2.0-flash que es el que te dio error 429 (significa que existe)
    # Si falla, espera y reintenta
    time.sleep(2) 
    response_text = client.models.generate_content(
        model="gemini-2.0-flash", 
        contents=prompt_completo
    ).text
    
    partes = response_text.split("SEPARADOR")
    if len(partes) >= 4:
        respuesta1 = partes[0].strip()
        respuesta2 = partes[1].strip()
        respuesta4 = partes[2].strip()
        descripcion = partes[3].strip()
    else:
        descripcion = response_text
        respuesta1 = "Ver descripción general."
        respuesta2 = "Ver descripción general."
        respuesta4 = "Ver descripción general."
    print("Texto generado con éxito.")
    
except Exception as e:
    print(f"Error generando texto: {e}")
    descripcion = "Vasija arqueológica de cerámica color rojizo con bordes desgastados."
    respuesta1 = "No disponible por error de conexión."
    respuesta2 = "No disponible por error de conexión."
    respuesta4 = "No disponible por error de conexión."

# MODELO 2: IMAGEN (Usamos el nombre de tu archivo original)
print("Generando imagen (Intentando con modelo original)...")
time.sleep(5) # Pausa larga para recuperar cuota

try:
    # Este es el nombre exacto que tenías en tu archivo original
    # Si este falla, el script usará una imagen blanca de respaldo, pero no se detendrá.
    response_img = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=f"Generame una imagen realista de: {descripcion[:400]}",
        config=types.GenerateContentConfig(response_modalities=["IMAGE"])
    )

    imagen_generada = False
    for part in response_img.candidates[0].content.parts:
        if part.inline_data:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save("Vasija.png")
            imagen_generada = True
            
    if imagen_generada:
        print("Imagen 'Vasija.png' generada correctamente.")
    else:
        print("El modelo respondió pero no envió imagen.")
        Image.new('RGB', (400, 200), color='white').save("Vasija.png")

except Exception as e:
    print(f"No se pudo generar imagen: {e}")
    print("Creando imagen de respaldo para el PDF...")
    Image.new('RGB', (400, 200), color='white').save("Vasija.png")

# -----------------------------------------------------------
# 4. CREACIÓN DEL PDF
# -----------------------------------------------------------
def crear_pdf_adaptado(nombre_pdf, titulo, texto1, texto2, texto4, descripcion, imagen1, imagen2, imagen3, imagen4):
    doc = SimpleDocTemplate(nombre_pdf, pagesize=letter,
                            topMargin=50, bottomMargin=50,
                            leftMargin=50, rightMargin=50)
    styles = getSampleStyleSheet()
    estilo_texto = ParagraphStyle("TextoPlanoAdaptado", fontName="Helvetica", fontSize=12, leading=16, alignment=TA_LEFT)
    estilo_subtitulo = ParagraphStyle("TextoPlanoAdaptado", fontName="Helvetica", fontSize=14, leading=16, alignment=TA_CENTER)
    
    story = []
    story.append(Paragraph(titulo, styles["Title"]))
    story.append(Spacer(1,12))
    
    story.append(Paragraph("Recreación Visual (IA)", estilo_subtitulo))
    story.append(Spacer(1,12))
    try:
        story.append(RLImage(imagen3, width=400, height=200))
    except:
        pass
    story.append(Spacer(1,12))
    story.append(Paragraph(descripcion, estilo_texto))
    
    story.append(Spacer(1,12))
    story.append(Paragraph("Análisis de Color", estilo_subtitulo))
    story.append(Spacer(1,12))
    story.append(Paragraph(texto1, estilo_texto))
    story.append(Spacer(1,12))
    story.append(RLImage(imagen1, width=400, height=200))
    
    story.append(Spacer(1,12))
    story.append(Paragraph("Análisis Decorativo", estilo_subtitulo))
    story.append(Spacer(1,12))
    story.append(Paragraph(texto2, estilo_texto))
    story.append(Spacer(1,12))
    story.append(RLImage(imagen2, width=400, height=200))
    
    story.append(Spacer(1,12))
    story.append(Paragraph("Análisis de Manufactura", estilo_subtitulo))
    story.append(Spacer(1,12))
    story.append(Paragraph(texto4, estilo_texto))
    story.append(Spacer(1,12))
    story.append(RLImage(imagen4, width=400, height=200))
    
    doc.build(story)

nombre_pdf = "Reto1_Visualizacion.pdf"
titulo = "Hallazgos Arqueológicos - Los Titanes"
crear_pdf_adaptado(nombre_pdf, titulo, respuesta1, respuesta2, respuesta4, descripcion, "F_colores.png", "F_tecnica_decorativa.png", "Vasija.png", "F_tecnica_manufactura.png")
print("Pdf generado correctamente :)")