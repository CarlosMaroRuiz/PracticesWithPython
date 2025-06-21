import sqlite3
from student.models.student import Student

def list_students():
    with sqlite3.connect("practica.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, grupo, grado FROM alumno")
        data_result = cursor.fetchall()
        return parserData(data_result)


def parserData(students):
    data_parsed = []
    for student in students:
        data_parsed.append(Student(name=student[1],grupo=student[2],grado=student[3]))
    return data_parsed