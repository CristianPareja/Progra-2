#clases y objetos en python

#clase es un plantilla que nos permite crear objetos



# class Persona:
#     pass #es un palabra reservada que me permite dejar las cosas en blanco

# #creamos o instanciamos objetos de esta clase
# #Un objeto es una instacia "concreta" de la clase
# #clase por referencia
# persona1 = Persona()
# persona2 = persona1

# print("Tipo de persona 1:",type(persona1))
# print("Direccion de memoria de persona 1:",persona1)
# print("Direccion de memoria de persona 2:",persona2)


# #creacion de atributos directa (no recomendado)
# persona1.nombre = "Danni"
# print(persona2.nombre)
# persona1.nombre = "Raquel"
# print(persona2.nombre)


# #No es ideal para crear muchas instancias y por eso existen los constructores
# persona3=Persona()
# persona3.nombre="Andres"

# class Auto:
#     pass

# auto1=Auto()
# auto2=Auto()

# auto1.marca = "Toyota"
# auto1.modelo = "Corolla"

# auto2.marca = "Chevrolet"
# auto2.modelo = "Camaro"

# print("auto 1", auto1.marca, auto1.modelo)
# print("auto 2", auto2.marca, auto2.modelo)

#BLOQUE 2 : Atributos, metodos y constructores

# class Persona:
    #constructor se ejecuta automaticamente en cada instancia del objeto
    # def __init__(self,nombre,edad):
    #     self.nombre = nombre
    #     self.edad = edad
    # #metodo de clase
    # def saludar(self):
    #     print(f"Hola mi nombre es:{self.nombre} y tengo {self.edad} anios ")

    # def es_mayor_de_edad(self):
    #     return self.edad > 17
    
    #creamos objetos con atributos definidos

# persona1 =Persona("Danni",30)
# persona2 =Persona("Nicole",28)
# persona3 =Persona("Raul",10)

# #usamos los metodos de las instancias

# persona1.saludar()
# persona2.saludar()

# Espersona1Mayor=persona1.es_mayor_de_edad()
# print("Es Danni mayor de edad?", Espersona1Mayor)

# Espersona1Mayor=persona3.es_mayor_de_edad()
# print("Es Raul mayor de edad?", Espersona1Mayor)

#self es una referencia al objeto actual
#los metodos son funciones de una clase
#los atributos son variables de una clase

#BLOQUE 3 : Pilares de la Programacion orientad a objetos POO

#abstraccion: abstraer o representar objetos de la vida real de manera simple (en una clase con atributos y metodos)
#las clases no tienen porque representar algo fisico
# class Transferencia:
#     origen
#     destino
#     cantidad
#abstraccion y encapsulamiento: El encapsulamiento se trata sobre cada uno de nuestros modulos solo tengo permitido el acceso y hacer cosas que requieren
# class Animal:
#     def __init__(self,nombre,especie):
#         self._nombre=nombre #proteger atributos
#         self._especie=especie
#         #nombre y especie solo son accesibles dentro del alcance de la clase

#     def describir(self):
#         print(f"Soy {self._nombre} y soy un {self._especie}")

#     #Snake case
#     def hacer_sonido(self):
#         print("Haciendo un sonido generico")

# perro = Animal("Toby","Can")
# perro.describir()
# #herencia : las subclases que heredan de Animal
# class Leon(Animal):
#     #automaticamente con herencia ya tengo disponibles los metodos de la clase padre
#     def __init__(self, nombre):
#         super().__init__(nombre, "leon")
# simba = Leon("simba")
# simba.describir()

# class Elefante(Animal):
#     def __init__(self, nombre):
#         super().__init__(nombre, "elefante")
    
#     #sobreescritura de metodos
#     def hacer_sonido(self):
#         print("pruuuuuu")
    
# Many = Elefante("Many")
# Many.describir()
# Many.hacer_sonido()

# class Empleado:
#     def __init__(self,nombre,cargo):
#         self._nombre=nombre #proteger atributos
#         self._cargo=cargo
#         #nombre y especie solo son accesibles dentro del alcance de la clase

#     def describir(self):
#         print(f"El empleado {self._nombre} trabaja en el area de: {self._cargo}")

#     #Snake case
#     def tipo_de_contrato(self):
#         print("El empleado tiene un contrato fijo")

# empleado1 = Empleado("Carlos","Produccion")
# empleado1.describir()
# empleado1.tipo_de_contrato()

# class empleado_temporal(Empleado):
#      def __init__(self, nombre):
#          super().__init__(nombre,"Financiero")
    
#      #sobreescritura de metodos
#      def tipo_de_contrato(self):
#          print("El empleado tiene un contrato temporal")
# empleado2 = empleado_temporal("Ana")
# empleado2.describir()
# empleado2.tipo_de_contrato()

# #polimorfismo
# class Figura:
#     def __init__(self,nombre):
#         self._nombre=nombre
#     def calcularPerimetro(self):
#         raise NotImplementedError("Esto debe ser llamado en la subclase")

# class Cuadrado(Figura):
#     def __init__(self, lado):
#         super().__init__("Cuadrado")
#         self._lado=lado
    
#     def calcularPerimetro(self):
#         return self.lado *4
# class Triangulo (Figura):

# class TrianguloEquilatero(Triangulo):



# objeto abstracto o clase 
# instancia (es un)
# compuesto (es parte de/tiene un)
# herencia (es un tipo de)

#Clase Padre
class TransferenciaBancaria: # (abstraccion)
    def __init__(self, titular, monto):
        self._titular = titular  #proteger atributos (encapsulamiento)
        self._monto = monto      #proteger atributos (encapsulamiento)

    def describir(self):
        print(f"El titular: {self._titular} tiene un monto de: {self._monto}")

    def tipo_de_transferencia(self):
        print("Tipo de transferencia: General")

#Clase Hija 1
class TransferenciaNormal(TransferenciaBancaria): # (herencia)
    def __init__(self, titular, monto):
        super().__init__(titular, monto)

t1 = TransferenciaNormal("Luis", 100)
t1.describir()
t1.tipo_de_transferencia()
print()
     
#Clase Hija 2
class TransferenciaInternacional(TransferenciaBancaria):
    def __init__(self, titular, monto, pais_destino):
        super().__init__(titular, monto)
        self._pais_destino = pais_destino

    def describir(self):
        super().describir()
        print(f"Pais destino: {self._pais_destino}")

    def tipo_de_transferencia(self):
        print("Transferencia internacional: requiere codigo secreto y verificacion adicional.")

t2 = TransferenciaInternacional("Maria", 500, "Estados Unidos")
t2.describir()
t2.tipo_de_transferencia()
print()

#Clase Hija 3
class Transferencialocal(TransferenciaBancaria):
    def __init__(self, titular, monto):
        super().__init__(titular, monto)

    def tipo_de_transferencia(self):
        print("Transferencia local: dentro del mismo banco.")

t3 = Transferencialocal("Pedro", 250)
t3.describir()
t3.tipo_de_transferencia()
print()