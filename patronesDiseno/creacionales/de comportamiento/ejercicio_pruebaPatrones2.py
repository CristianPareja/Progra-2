class Tesis:
    def __init__(self):
        self.contenido = ""

    def escribir(self, texto):
        self.contenido += texto + "\n"

    def crear_memento(self):
        return Memento(self.contenido)

    def restaurar(self, memento):
        self.contenido = memento.estado

    def mostrar(self):
        print("\n Contenido actual de la tesis:\n" + self.contenido)


class Memento:
    def __init__(self, estado):
        self.estado = estado


def menu_tesis():
    tesis = Tesis()
    versiones = []

    while True:
        print("\n=== TERMINA PORFIN DE TESIS ===")
        print("1. Escribir nueva versión")
        print("2. Mostrar versión actual")
        print("3. Restaurar versión anterior")
        print("4. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            texto = input("Escribe el contenido de la nueva versión: ")
            tesis.escribir(texto)
            versiones.append(tesis.crear_memento())
            print(f" Versión {len(versiones)} guardada.")
        elif opcion == "2":
            tesis.mostrar()
        elif opcion == "3":
            if versiones:
                try:
                    num = int(input(f"Ingrese número de versión a restaurar (1 - {len(versiones)}): "))
                    if 1 <= num <= len(versiones):
                        tesis.restaurar(versiones[num - 1])
                        print(f"Restaurado a la versión {num}.")
                    else:
                        print("Número inválido.")
                except ValueError:
                    print("Ingresa un número válido.")
            else:
                print("No hay versiones guardadas aún.")
        elif opcion == "4":
            print("Saliendo")
            break
        else:
            print("Opción no válida. Intenta otra vez.")

menu_tesis()

