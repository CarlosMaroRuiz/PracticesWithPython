class Student:
    def __init__(self,name,grupo,grado):
        self.name = name
        self.grupo = grupo
        self.grado = grado
    def student_mapper(self):
        return  {
                'name': self.name,
                'grupo': self.grupo,
                'grado': self.grado
            }