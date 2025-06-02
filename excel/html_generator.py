import os
import webbrowser
import markdown
import base64
import io
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
matplotlib.use('Agg')  # Usar backend no interactivo para evitar ventanas emergentes

def generate_html_from_markdown(md_content: str, title: str = "Reporte DeepSeek", data=None) -> str:
    """Convierte markdown a HTML con mejor formato y gráficas generadas con matplotlib"""
    
    # Pre-procesamiento del markdown para mejorar formato
    md_content = md_content.replace('**', '### ')  # Convertir ** a encabezados H3
    md_content = md_content.replace('- ', '\n- ')  # Asegurar que cada elemento de lista tiene su propio salto de línea
    
    # Convertir markdown a HTML con extensiones adicionales
    html_body = markdown.markdown(
        md_content, 
        extensions=[
            "tables", 
            "fenced_code", 
            "codehilite", 
            "nl2br",  # Convierte saltos de línea a <br>
            "sane_lists",  # Mejor manejo de listas
            "extra"  # Conjunto de extensiones adicionales
        ]
    )
    
    # Generar resumen visual con tarjetas de estadísticas
    stats_cards = ""
    if data and data['temperaturas']:
        # Calcular estadísticas
        temp_avg = sum(data['temperaturas']) / len(data['temperaturas'])
        temp_min = min(data['temperaturas'])
        temp_max = max(data['temperaturas'])
        alertas = data['estados'].count('Alerta')
        normales = len(data['estados']) - alertas
        total_readings = len(data['temperaturas'])
        
        # Generar HTML para tarjetas de estadísticas
        stats_cards = f"""
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-value">{temp_avg:.1f}°C</div>
                <div class="stat-label">Temperatura Promedio</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">{temp_min}°C</div>
                <div class="stat-label">Temperatura Mínima</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">{temp_max}°C</div>
                <div class="stat-label">Temperatura Máxima</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-value">{alertas}</div>
                <div class="stat-label">Alertas Detectadas</div>
            </div>
            
            <div class="stat-card highlight">
                <div class="stat-value">{(normales/total_readings*100):.0f}%</div>
                <div class="stat-label">Lecturas Normales</div>
            </div>
        </div>
        """
    
    # Generar gráfica de barras
    chart_html = generate_bar_chart(data) if data else ""
    
    # Generar gráfica de pastel
    pie_html = generate_pie_chart(data) if data else ""
    
    # Generar tabla de datos
    data_table = generate_data_table(data) if data else ""
    
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Source+Code+Pro&display=swap');

            body {{
                font-family: 'Roboto', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f8f9fa;
                color: #343a40;
                line-height: 1.7;
            }}

            .container {{
                max-width: 960px;
                margin: 40px auto;
                background-color: #ffffff;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            }}

            h1, h2, h3, h4, h5, h6 {{
                color: #0056b3;
                margin-top: 1.5em;
                margin-bottom: 0.8em;
                border-bottom: 2px solid #e9ecef;
                padding-bottom: 0.3em;
            }}

            h1 {{
                font-size: 2.5em;
                border-bottom-width: 3px;
                margin-top: 0;
            }}

            h2 {{
                font-size: 2em;
            }}

            h3 {{
                font-size: 1.5em;
                margin-top: 2em;
                font-weight: 600;
            }}

            p {{
                margin-bottom: 1.2em;
            }}

            a {{
                color: #007bff;
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
                overflow: hidden;
                border: 1px solid #dee2e6;
            }}

            th, td {{
                padding: 12px 15px;
                text-align: left;
                border-bottom: 1px solid #dee2e6;
            }}

            th {{
                background-color: #e9ecef;
                color: #495057;
                font-weight: 700;
                text-transform: uppercase;
                font-size: 0.85em;
            }}

            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}

            tr:hover {{
                background-color: #e2e6ea;
            }}

            code {{
                font-family: 'Source Code Pro', monospace;
                background-color: #e9ecef;
                padding: 0.2em 0.4em;
                margin: 0;
                font-size: 85%;
                border-radius: 3px;
                color: #c7254e;
            }}

            pre {{
                background: #282c34;
                color: #abb2bf;
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
                color: #6c757d;
            }}

            strong {{
                color: #0056b3;
                font-weight: 700;
            }}

            em {{
                color: #495057;
                font-style: italic;
            }}

            hr {{
                border: none;
                border-top: 1px solid #dee2e6;
                margin: 40px 0;
            }}

            ul, ol {{
                margin-bottom: 1.2em;
                padding-left: 25px;
            }}

            li {{
                margin-bottom: 8px;
                line-height: 1.6;
            }}
            
            /* Estilos para las gráficas */
            .chart-container {{
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
                border-radius: 8px;
                padding: 25px;
                margin: 30px 0;
                background-color: white;
                transition: transform 0.3s ease;
            }}
            
            .chart-container:hover {{
                transform: translateY(-5px);
            }}
            
            .chart-container h3 {{
                color: #0056b3;
                margin-top: 0;
                border-bottom: 2px solid #e9ecef;
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            
            .chart-image {{
                max-width: 100%;
                height: auto;
                display: block;
                margin: 0 auto;
            }}
            
            /* Estilos para tarjetas de estadísticas */
            .stats-container {{
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                margin: 30px 0;
            }}
            
            .stat-card {{
                flex: 1;
                min-width: 150px;
                background-color: #ffffff;
                border-radius: 8px;
                padding: 20px;
                margin: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}
            
            .stat-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }}
            
            .stat-card.highlight {{
                background-color: #f0f9ff;
                border-left: 4px solid #007bff;
            }}
            
            .stat-value {{
                font-size: 2.2em;
                font-weight: 700;
                color: #0056b3;
                margin-bottom: 10px;
            }}
            
            .stat-label {{
                font-size: 0.9em;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            /* Estilos para la tabla de datos */
            .data-table-container {{
                margin: 30px 0;
                overflow-x: auto;
            }}
            
            .data-table {{
                width: 100%;
                border-collapse: collapse;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                overflow: hidden;
            }}
            
            .data-table th {{
                background-color: #0056b3;
                color: white;
                padding: 15px;
                text-align: left;
            }}
            
            .data-table td {{
                padding: 12px 15px;
                border-bottom: 1px solid #dee2e6;
            }}
            
            .data-table tr:last-child td {{
                border-bottom: none;
            }}
            
            .data-table tr.alert {{
                background-color: #fff5f5;
            }}
            
            .data-table tr.alert td:nth-child(3) {{
                color: #e53e3e;
                font-weight: bold;
            }}
            
            .data-table tr.normal td:nth-child(3) {{
                color: #38a169;
            }}

            /* Mejoras para dispositivos móviles */
            @media (max-width: 768px) {{
                .container {{
                    padding: 20px;
                    margin: 20px;
                }}
                
                .stat-card {{
                    min-width: 120px;
                }}
                
                .stat-value {{
                    font-size: 1.8em;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{title}</h1>
            
            <!-- Resumen visual con tarjetas -->
            {stats_cards}
            
            <!-- Contenido principal del análisis -->
            <div class="main-content">
                {html_body}
            </div>
            
            <!-- Tabla de datos completa -->
            {data_table}
            
            <!-- Sección de gráficas -->
            <h2>Visualizaciones</h2>
            
            <div class="chart-container">
                <h3>Temperaturas por Ubicación</h3>
                {chart_html}
            </div>
            
            <div class="chart-container">
                <h3>Distribución de Estados</h3>
                {pie_html}
            </div>
        </div>
    </body>
    </html>
    """
    return html

def generate_bar_chart(data):
    """Genera una gráfica de barras con matplotlib y la devuelve como HTML img"""
    if not data or not data['temperaturas']:
        return "<p>No hay datos disponibles para generar la gráfica</p>"
    
    plt.figure(figsize=(10, 6))
    
    # Crear un color especial para alertas
    colors = ['#4BC0C0' if estado == 'Normal' else '#FF6384' 
              for estado in data['estados']]
    
    # Configurar el estilo
    plt.style.use('ggplot')
    
    # Crear la gráfica de barras
    bars = plt.bar(data['ubicaciones'], data['temperaturas'], color=colors, width=0.6)
    
    # Añadir línea de promedio
    avg_temp = sum(data['temperaturas']) / len(data['temperaturas'])
    plt.axhline(y=avg_temp, color='#333333', linestyle='--', alpha=0.7, 
                label=f'Promedio: {avg_temp:.1f}°C')
    
    # Añadir valores sobre las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{height}°C',
                ha='center', va='bottom', fontweight='bold')
    
    # Estilizar la gráfica
    plt.title('Temperaturas por Ubicación', fontsize=15, pad=20)
    plt.ylabel('Temperatura (°C)', fontsize=12)
    plt.xlabel('Ubicación', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.legend()
    
    # Añadir un poco de espacio arriba para los valores
    max_temp = max(data['temperaturas'])
    plt.ylim(top=max_temp + 1.5)
    
    # Ajustar márgenes
    plt.tight_layout()
    
    # Guardar la figura en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    # Codificar la imagen en base64
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    # Cerrar la figura para liberar memoria
    plt.close()
    
    # Devolver HTML img con la imagen en base64
    return f'<img src="data:image/png;base64,{img_str}" class="chart-image" alt="Gráfica de temperaturas por ubicación">'

def generate_pie_chart(data):
    """Genera una gráfica de pastel con matplotlib y la devuelve como HTML img"""
    if not data or not data['estados']:
        return "<p>No hay datos disponibles para generar la gráfica</p>"
    
    plt.figure(figsize=(8, 8))
    
    # Contar el número de alertas y lecturas normales
    alertas = data['estados'].count('Alerta')
    normales = data['estados'].count('Normal')
    
    # Si no hay alertas o todo son alertas, ajustar para que se vea el gráfico
    if alertas == 0:
        alertas = 0.01  # Valor muy pequeño para que se vea en el gráfico
    if normales == 0:
        normales = 0.01
    
    # Crear gráfica de pastel
    labels = ['Normal', 'Alerta']
    sizes = [normales, alertas]
    colors = ['#4BC0C0', '#FF6384']
    explode = (0, 0.1)  # Resaltar la porción de alertas
    
    # Configurar el estilo
    plt.style.use('ggplot')
    
    # Crear el gráfico de pastel
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90,
            textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    # Asegurar que el círculo es un círculo
    plt.axis('equal')
    
    # Añadir título
    plt.title('Distribución de Estados', fontsize=15, pad=20)
    
    # Guardar la figura en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    
    # Codificar la imagen en base64
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    # Cerrar la figura para liberar memoria
    plt.close()
    
    # Devolver HTML img con la imagen en base64
    return f'<img src="data:image/png;base64,{img_str}" class="chart-image" alt="Gráfica de distribución de estados">'

def generate_data_table(data):
    """Genera una tabla HTML con todos los datos"""
    if not data or not data['ubicaciones']:
        return ""
    
    table_rows = ""
    for i in range(len(data['ubicaciones'])):
        estado_class = "alert" if data['estados'][i] == 'Alerta' else "normal"
        table_rows += f"""
        <tr class="{estado_class}">
            <td>{i+1}</td>
            <td>{data['ubicaciones'][i]}</td>
            <td>{data['temperaturas'][i]}°C</td>
            <td>{data['estados'][i]}</td>
        </tr>
        """
    
    table_html = f"""
    <div class="data-table-container">
        <h3>Datos Completos</h3>
        <table class="data-table">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Ubicación</th>
                    <th>Temperatura</th>
                    <th>Estado</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    """
    
    return table_html

def save_and_open_html(html_content: str, filename: str = "resultado.html"):
    """Guarda el contenido HTML en un archivo y lo abre en el navegador"""
    filepath = os.path.abspath(filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    webbrowser.open(f"file://{filepath}")