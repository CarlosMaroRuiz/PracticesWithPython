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
Analiza la siguiente tabla de lecturas de temperatura y genera un reporte de análisis estadístico. 
Incluye promedios, desviaciones si es posible, cuántas alertas hubo, valores máximos y mínimos, y cualquier otro hallazgo relevante.

{tabla}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "Eres un analista de datos experto."},
            {"role": "user", "content": prompt}
        ],
        stream=False
    )

    return response.choices[0].message.content

