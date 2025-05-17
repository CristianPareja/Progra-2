#Clase Padre
class Educacion: # (abstraccion)
    def __init__(self, estudiantes,materias, profesor):
        self._materias = materias  #proteger atributos (encapsulamiento)
        self._profesor = profesor      #proteger atributos (encapsulamiento)
        self._estudiantes = estudiantes      #proteger atributos (encapsulamiento)

    def describir(self):
        print(f"El estudiante: {self._estudiantes} tiene la materia de {self._materias} con el profesor {self._profesor} ")

    def estado_matriculado(self):
        print("Estado estudiante: matriculado")

#Subclase 1
class Curso(Educacion): # (herencia)
    def __init__(self, estudiantes, materias, profesor):
        super().__init__(estudiantes,materias, profesor)

t1 = Curso("Mauricio", "Progra 2", "Danny Brito")
t1.describir()
t1.estado_matriculado()
print()
     
#Subclase 2
class Curso_Online(Educacion):
    def __init__(self, estudiantes,materias, profesor,plataforma):
        super().__init__(estudiantes,materias, profesor)
        self._plataforma = plataforma

    def describir(self):
        super().describir()
        print(f"Plataforma: {self._plataforma}")

    def estado_matriculado(self):
        print("Estado estudiante: Matricula Extraordinaria")

t2 = Curso_Online("Franklin", "TICS", "Patricio Alvear","teams")
t2.describir()
t2.estado_matriculado()
print()

#Subclase 3
class Curso_presencial(Educacion):
    def __init__(self, estudiantes,materias, profesor,aula):
        super().__init__(estudiantes,materias, profesor)
        self._aula = aula

    def describir(self):
        super().describir()
        print(f"Aula: {self._aula}")

    def estado_matriculado(self):
        print("Estado estudiante: Matricula Ordinaria")
        

t3 = Curso_presencial("Erick", "Base de datos", "Jorge Galarza","Aula 303")
t3.describir()
t3.estado_matriculado()
print()