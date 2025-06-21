from student.services.add_student import add_student
from student.models.student import Student
#iu uses service

def add_student_iu():
    name = input("ingrese el nombre del estudiante")
    grupo = input("Ingrese el grupo del estudiante")
    grado = input("ingrese el grado del estudiante")
    add_student(Student(name,grupo,grado))