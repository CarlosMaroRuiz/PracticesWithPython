import openpyxl
from deepseek_request import deepseek_request
from html_generator import generate_html_from_markdown,save_and_open_html

# Cargar el archivo
wb = openpyxl.load_workbook("sensores_temperatura.xlsx")


contenido = ""
for sheet in wb.sheetnames:
    hoja = wb[sheet]
    for fila in hoja.iter_rows(values_only=True):
        fila_texto = "\t".join([str(celda) if celda is not None else "" for celda in fila])
        contenido += fila_texto + "\n"

# el resultado que nos dara nuestra funcion de la api deepseek
markdown_result = deepseek_request(contenido)

# Convertir y mostrar
html = generate_html_from_markdown(markdown_result, title="Análisis de Sensores de Temperatura")
save_and_open_html(html)
