# Mucha gente lo considera un antipatron
##creacionales, estructurales y comportamiento patrones de diseno************************][0]
# Que hace?
# Asegura que una clase tenga una unica instancia

# Cuando solo debe existir un objeto de cierta clase (ejemplo la ventana de Tkinter)
# cuando necesitamos un logger global, un controlador global, 
# una conexion unica a la BDD, una sola sesion en un cajero automatico

# Analogia
# el refri de nuestra casa
# siempre solo tenemos uno
# al comprar leche, aumentamos ese producto en el refri
# al acabarnos los huevos, ese producto se vacía de la misma refri
# no se crean ni se destruyen instancias
# varias personas agregan o usan cosas de la misma refri

# Problema, creamos varias instancias cuando solo necesito una misma siempre
class Configuracion:
    _instancia = None # atributo de clase

    # Metodo especial que se ejecuta antes del __init__
    def __new__(cls):
        if cls._instancia is None:
            print("Creando Nueva Instancia")
            cls._instancia = super().__new__(cls)
        else:
            print("Usaremos la instancia ya existente")
        return cls._instancia
    
    def __init__(self):
        self.modo = "oscuro"

a = Configuracion()
b = Configuracion()

print(a is b) # Imprime True, ambos son la misma instancia
print(a.modo) #oscuro
b.modo = "claro"
print(a.modo)
