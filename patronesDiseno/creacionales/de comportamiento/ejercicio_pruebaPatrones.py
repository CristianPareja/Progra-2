class Mediador:
    def enviar(self, mensaje, emisor):
        pass

class Empleado:
    def __init__(self, nombre, mediador):
        self.nombre = nombre
        self.mediador = mediador

    def enviar(self, mensaje):
        print(f"\n{self.nombre} dice: {mensaje}")
        self.mediador.enviar(mensaje, self)

    def recibir(self, mensaje):
        print(f"{self.nombre} recibe: {mensaje}")


class CoordinadorProyecto(Mediador):
    def __init__(self):
        self.empleados = []

    def registrar(self, empleado):
        self.empleados.append(empleado)

    def enviar(self, mensaje, emisor):
        for empleado in self.empleados:
            if empleado != emisor:
                empleado.recibir(f"{emisor.nombre}: {mensaje}")

class Desarrollador(Empleado):
    pass

class Tester(Empleado):
    pass

class LiderProyecto(Empleado):
    pass

def menu_oficina():
    coordinador = CoordinadorProyecto()

    dev = Desarrollador("Cris (Desarrollador)", coordinador)
    tester = Tester("Luis (Tester)", coordinador)
    lider = LiderProyecto("Danni (Lider)", coordinador)

    coordinador.registrar(dev)
    coordinador.registrar(tester)
    coordinador.registrar(lider)

    empleados = {
        "1": dev,
        "2": tester,
        "3": lider
    }

    while True:
        print("\n----------Oficina Tres Patitos ---------")
        print("1. Cris (Desarrollador)")
        print("2. Luis (Tester)")
        print("3. Danni (Líder de Proyecto)")
        print("4. Salir")
        opcion = input("¿Quién va a enviar un mensaje? ")

        if opcion in empleados:
            mensaje = input("Escribe tu mensaje: ")
            empleados[opcion].enviar(mensaje)
        elif opcion == "4":
            print("Saliendo")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

menu_oficina()