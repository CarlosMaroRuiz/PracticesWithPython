import sqlite3
from migrations.alumno import alumno_table

def execute_migrations():
    #lo que hace connect se conecta al nombre de la db caso no exista lo crea
    #trabajando con with
    with sqlite3.connect("practica.db") as conexion:
    
      """ 
    el metodo cursor es un objeto que nos permite ejecutar consultas de una base de datos
       """
    cursor = conexion.cursor()
    cursor.execute(alumno_table)




