import os
from dotenv import load_dotenv
from openai import OpenAI

# Cargar variables de entorno
load_dotenv()

def deepseek_request(tabla):
    api_key = os.getenv("DEEPSEEK_API")
    if not api_key:
        raise ValueError("La clave DEEPSEEK_API no está definida en el archivo .env")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    prompt = f"""
Analiza la siguiente tabla de lecturas de temperatura y genera un reporte detallado de análisis estadístico.

Estructura el análisis de la siguiente manera:
1. Resumen General: Total de lecturas, rango temporal, ubicaciones monitoreadas.
2. Análisis de Temperaturas: Promedio, valores mínimos y máximos, desviación estándar y análisis detallado por ubicación.
3. Análisis de Alertas: Total de alertas, porcentaje, ubicaciones afectadas y posibles causas.
4. Hallazgos Relevantes: Patrones, anomalías, relaciones entre ubicaciones y temperaturas.
5. Recomendaciones: Sugerencias basadas en los datos analizados.

Usa formato markdown para estructurar tu respuesta con encabezados, listas y énfasis donde corresponda.
No incluyas código de visualización, ya que generaremos las gráficas automáticamente.

Tabla de datos:
{tabla}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Eres un analista de datos experto especializado en monitoreo ambiental y sistemas de control de temperatura."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )

    return response.choices[0].message.content