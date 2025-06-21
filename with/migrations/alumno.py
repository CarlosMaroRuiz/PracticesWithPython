from migrations.consultas.base import base_query_create
alumno_table = f""" 
   {base_query_create("alumno")}(
   id INTEGER PRIMARY KEY, 
   name TEXT,
   grupo TEXT,
   grado INTEGER
   )
"""