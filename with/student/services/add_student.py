from student.models.student import Student
import sqlite3

def add_student(student: Student) -> bool:
    
    if not student or not isinstance(student, Student):
        print("Error: El objeto estudiante no es válido")
        return False
        
    try:
        student_data = student.student_mapper()
        """ 
        El values se puede usar ya que es una propiedad de los diccionario y como nuestro
        mapper es un diccionario por eso podemos aplicarlo
        """
        if not all(student_data.values()):
            print("Error: Todos los campos del estudiante deben contener valores")
            return False
            
        with sqlite3.connect("practica.db") as conexion:
            cursor = conexion.cursor()
            
            cursor.execute("""
                INSERT INTO alumno (name, grupo, grado)
                VALUES (:name, :grupo, :grado)
            """, student_data)
            
            conexion.commit()
            print(f"Estudiante {student.name} agregado exitosamente con ID: {cursor.lastrowid}")
            return True
    #exepciones especificas de sqlite       
    except sqlite3.IntegrityError as e:
        print(f"Error de integridad en la base de datos: {e}")
        return False
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False