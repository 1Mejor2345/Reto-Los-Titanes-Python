# 🏺 Proyecto Arqueológico Los Titanes: Análisis de Datos e IA

Este proyecto automatiza el procesamiento de datos arqueológicos provenientes de excavaciones (ficticias o reales). Realiza limpieza de datos, genera visualizaciones estadísticas, utiliza Inteligencia Artificial (Google Gemini) para interpretar hallazgos y reconstruir visualmente vasijas, y exporta un reporte final en PDF.

## 🚀 Funcionalidades

1.  **ETL (Extracción, Transformación y Carga):** Limpia y estructura datos crudos desde Excel (`LOS_TITANES_RETO1.py`).
2.  **Análisis Estadístico:** Genera gráficos de barras sobre frecuencia de colores, técnicas de manufactura y decoración.
3.  **Inteligencia Artificial Generativa:**
    * Utiliza **Google Gemini** para analizar patrones en los datos.
    * Genera descripciones textuales y reconstrucciones visuales (imágenes) de las vasijas halladas.
4.  **Reporte Automatizado:** Consolida toda la información y gráficos en un archivo PDF (`Reto1_Visualizacion.pdf`).

## 📋 Requisitos Previos

Necesitas tener instalado **Python 3.10** o superior.

### Instalación de dependencias

Ejecuta el siguiente comando para instalar todas las librerías necesarias:

```bash
pip install pandas openpyxl matplotlib reportlab python-dotenv google-genai Pillow