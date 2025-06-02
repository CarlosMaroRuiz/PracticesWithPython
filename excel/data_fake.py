import openpyxl
import random
import string
import time
from faker import Faker
import os
import psutil

def generar_excel_contactos(filename="contactos.xlsx", num_registros=100000, porcentaje_errores=10):
    """
    Genera un archivo Excel con datos de contactos, incluyendo errores deliberados.
    
    Args:
        filename (str): Nombre del archivo Excel a generar
        num_registros (int): Número de registros a generar
        porcentaje_errores (int): Porcentaje de registros que tendrán errores (0-100)
    """
    print(f"🚀 Generando archivo Excel con {num_registros:,} contactos...")
    print(f"🐛 Se incluirán aproximadamente {porcentaje_errores}% de registros con errores")
    
    start_time = time.time()
    
    # Inicializar Faker para datos aleatorios
    fake = Faker('es_MX')
    
    # Crear un nuevo libro Excel con optimización para escritura
    wb = openpyxl.Workbook(write_only=True)
    sheet = wb.create_sheet("Contactos")
    
    # Añadir encabezados
    sheet.append(["ClaveCliente", "Nombre", "Correo", "TelefonoContacto"])
    
    # Lista de proveedores de correo permitidos
    proveedores_correo = ["gmail.com", "yahoo.com", "hotmail.com", 
                         "outlook.com", "live.com", "icloud.com", "protonmail.com"]
    
    # Tipos de errores a introducir
    tipos_errores = [
        "clave_vacia",
        "clave_no_numerica",
        "nombre_con_numeros",
        "nombre_vacio",
        "correo_sin_arroba",
        "correo_proveedor_invalido",
        "telefono_corto",
        "telefono_largo",
        "telefono_con_letras"
    ]
    
    # Conjunto para mantener las claves de cliente ya generadas
    claves_generadas = set()
    
    # Contadores para estadísticas
    registros_correctos = 0
    registros_con_errores = 0
    errores_por_tipo = {error: 0 for error in tipos_errores}
    
    # Función para mostrar estadísticas de uso de memoria
    def mostrar_memoria():
        proceso = psutil.Process(os.getpid())
        memoria = proceso.memory_info().rss / 1024 / 1024  # en MB
        return f"Memoria: {memoria:.2f} MB"
    
    # Lote de filas para escribir de forma eficiente
    batch_size = 10000
    rows_batch = []
    
    # Generar datos
    for i in range(1, num_registros + 1):
        # Decidir si este registro tendrá errores
        tiene_error = random.randint(1, 100) <= porcentaje_errores
        
        # Base para un registro correcto
        clave_cliente = random.randint(1, 9999999)  # Número positivo
        while clave_cliente in claves_generadas:
            clave_cliente = random.randint(1, 9999999)
        claves_generadas.add(clave_cliente)
        
        nombre = fake.name()
        
        usuario_correo = nombre.lower().replace(" ", ".") + str(random.randint(1, 999))
        usuario_correo = ''.join(c for c in usuario_correo if c.isalnum() or c == '.')
        proveedor = random.choice(proveedores_correo)
        correo = f"{usuario_correo}@{proveedor}"
        
        telefono = ''.join(random.choice(string.digits) for _ in range(10))
        
        # Si debe tener error, introducir uno aleatorio
        if tiene_error:
            tipo_error = random.choice(tipos_errores)
            errores_por_tipo[tipo_error] += 1
            
            if tipo_error == "clave_vacia":
                clave_cliente = ""
            elif tipo_error == "clave_no_numerica":
                clave_cliente = "ABC" + str(clave_cliente)
            elif tipo_error == "nombre_con_numeros":
                nombre = nombre + "123"
            elif tipo_error == "nombre_vacio":
                nombre = ""
            elif tipo_error == "correo_sin_arroba":
                correo = correo.replace("@", "")
            elif tipo_error == "correo_proveedor_invalido":
                correo = f"{usuario_correo}@empresa-local.com"
            elif tipo_error == "telefono_corto":
                telefono = telefono[:random.randint(5, 8)]
            elif tipo_error == "telefono_largo":
                telefono = telefono + ''.join(random.choice(string.digits) for _ in range(random.randint(1, 5)))
            elif tipo_error == "telefono_con_letras":
                pos = random.randint(0, len(telefono) - 1)
                telefono = telefono[:pos] + random.choice(string.ascii_letters) + telefono[pos+1:]
            
            registros_con_errores += 1
        else:
            registros_correctos += 1
        
        # Añadir fila al lote
        rows_batch.append([clave_cliente, nombre, correo, telefono])
        
        # Si el lote está completo, escribirlo y limpiar
        if len(rows_batch) >= batch_size:
            for row in rows_batch:
                sheet.append(row)
            rows_batch = []
            
            # Liberar memoria periódicamente
            if i % (batch_size * 10) == 0:
                claves_generadas = set()  # Liberar memoria de claves
            
            # Mostrar progreso cada cierta cantidad de registros
            if i % (batch_size * 5) == 0:
                elapsed = time.time() - start_time
                registros_por_segundo = i / elapsed
                tiempo_restante = (num_registros - i) / registros_por_segundo if registros_por_segundo > 0 else 0
                
                print(f"✅ Generados {i:,} contactos ({i/num_registros*100:.1f}%) - "
                      f"Velocidad: {registros_por_segundo:.1f} reg/s - "
                      f"Tiempo restante: {tiempo_restante/60:.1f} min - "
                      f"{mostrar_memoria()}")
    
    # Escribir el lote final si queda algo
    for row in rows_batch:
        sheet.append(row)
    
    # Guardar el archivo
    print(f"💾 Guardando archivo Excel... (esto puede tomar varios minutos)")
    wb.save(filename)
    
    elapsed = time.time() - start_time
    
    # Mostrar estadísticas
    print("\n📊 ESTADÍSTICAS DE GENERACIÓN:")
    print(f"✅ Archivo Excel generado exitosamente: {filename}")
    print(f"⏱️ Tiempo total: {elapsed:.2f} segundos ({elapsed/60:.2f} minutos)")
    print(f"📊 Registros generados: {num_registros:,}")
    print(f"✓ Registros correctos: {registros_correctos:,} ({registros_correctos/num_registros*100:.1f}%)")
    print(f"✗ Registros con errores: {registros_con_errores:,} ({registros_con_errores/num_registros*100:.1f}%)")
    
    print("\n🐛 DISTRIBUCIÓN DE ERRORES:")
    for tipo, cantidad in errores_por_tipo.items():
        print(f"- {tipo}: {cantidad:,} ({cantidad/registros_con_errores*100:.1f}%)")

if __name__ == "__main__":
    # Configuración para 100,000 registros
    NOMBRE_ARCHIVO = "contactos_100k.xlsx"
    NUMERO_REGISTROS = 100000   # 100 mil registros
    PORCENTAJE_ERRORES = 15     # 15% de registros tendrán errores
    
    # Generar Excel
    generar_excel_contactos(NOMBRE_ARCHIVO, NUMERO_REGISTROS, PORCENTAJE_ERRORES)