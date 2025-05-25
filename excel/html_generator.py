import os
import webbrowser
import markdown

def generate_html_from_markdown(md_content: str, title: str = "Reporte DeepSeek") -> str:
    """Convierte markdown a HTML e incrusta en un template con estilo mejorado"""
    html_body = markdown.markdown(md_content, extensions=["tables", "fenced_code", "codehilite"])

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Source+Code+Pro&display=swap');

            body {{
                font-family: 'Roboto', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f8f9fa; /* Un gris muy claro */
                color: #343a40; /* Gris oscuro para texto */
                line-height: 1.7;
            }}

            .container {{
                max-width: 960px;
                margin: 40px auto;
                background-color: #ffffff; /* Fondo blanco para el contenido */
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: #0056b3; /* Un azul más vibrante */
                margin-top: 1.5em;
                margin-bottom: 0.8em;
                border-bottom: 2px solid #e9ecef; /* Línea sutil bajo los títulos */
                padding-bottom: 0.3em;
            }}

            h1 {{
                font-size: 2.5em;
                border-bottom-width: 3px;
            }}

            h2 {{
                font-size: 2em;
            }}

            h3 {{
                font-size: 1.5em;
            }}

            p {{
                margin-bottom: 1.2em;
            }}

            a {{
                color: #007bff; /* Azul estándar para enlaces */
                text-decoration: none;
            }}

            a:hover {{
                color: #0056b3;
                text-decoration: underline;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 25px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                border-radius: 5px;
                overflow: hidden; /* Para que el border-radius afecte a th/td */
                border: 1px solid #dee2e6; /* Borde sutil general */
            }}

            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #dee2e6; /* Líneas horizontales */
            }}

            th {{
                background-color: #e9ecef; /* Fondo gris claro para cabeceras */
                color: #495057; /* Texto más oscuro para cabeceras */
                font-weight: 700;
                text-transform: uppercase;
                font-size: 0.85em;
            }}

            tr:nth-child(even) {{
                background-color: #f8f9fa; /* Filas alternas con color sutil */
            }}

            tr:hover {{
                background-color: #e2e6ea; /* Efecto hover */
            }}

            code {{
                font-family: 'Source Code Pro', monospace;
                background-color: #e9ecef;
                padding: 0.2em 0.4em;
                margin: 0;
                font-size: 85%;
                border-radius: 3px;
                color: #c7254e; /* Color para código inline */
            }}

            pre {{
                background: #282c34; /* Fondo oscuro para bloques de código */
                color: #abb2bf; /* Texto claro */
                padding: 20px;
                display: block;
                overflow-x: auto;
                border-radius: 6px;
                font-family: 'Source Code Pro', monospace;
                font-size: 0.9em;
                margin-bottom: 20px;
                border: 1px solid #212529;
                box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);
            }}

            pre code {{
                padding: 0;
                font-size: inherit;
                color: inherit;
                background: none;
            }}

            blockquote {{
                border-left: 5px solid #007bff;
                background-color: #f8f9fa;
                padding: 15px 20px;
                margin: 20px 0;
                font-style: italic;
                color: #6c757d; /* Gris para citas */
            }}

            strong {{
                color: #212529; /* Casi negro para énfasis fuerte */
                font-weight: 700;
            }}

            em {{
                color: #495057; /* Gris oscuro para énfasis */
                font-style: italic;
            }}

            hr {{
                border: none;
                border-top: 1px solid #dee2e6; /* Línea divisoria más sutil */
                margin: 40px 0;
            }}

            ul, ol {{
                margin-bottom: 1.2em;
                padding-left: 20px;
            }}

            li {{
                margin-bottom: 0.5em;
            }}

        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            {html_body}
        </div>
    </body>
    </html>
    """
    return html

def save_and_open_html(html_content: str, filename: str = "resultado.html"):
    """Guarda el contenido HTML en un archivo y lo abre en el navegador"""
    # Asegúrate de que la ruta sea absoluta para evitar problemas con file://
    filepath = os.path.abspath(filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    # Usa file:// con la ruta absoluta
    webbrowser.open(f"file://{filepath}")

