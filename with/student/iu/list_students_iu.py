from student.services.list_student import list_students

def list_students_iu():
    for student in list_students():
        print("Estudiante:",student.student_mapper())
    