import tkinter as tk

# Clase Nodo - representa cada elemento de la lista
class Nodo:
    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None

# Clase ListaLigada - estructura principal que contiene los nodos
class ListaLigada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if not self.cabeza:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo

    def mostrar(self):
        valores = []
        actual = self.cabeza
        while actual:
            valores.append(str(actual.dato))
            actual = actual.siguiente
        return " → ".join(valores) + " → None" if valores else "Lista: vacía"

    def buscar(self, valor):
        actual = self.cabeza
        while actual:
            if actual.dato == valor:
                return True
            actual = actual.siguiente
        return False

    def eliminar(self, valor):
        actual = self.cabeza
        anterior = None

        while actual:
            if actual.dato == valor:
                if anterior is None:
                    self.cabeza = actual.siguiente
                else:
                    anterior.siguiente = actual.siguiente
                return True
            anterior = actual
            actual = actual.siguiente

        return False

# Instancia global de la lista
mi_lista = ListaLigada()

# Funciones para la interfaz
def agregar_nodo():
    valor = entrada.get()
    if valor.strip() == "":
        return
    mi_lista.agregar(valor)
    entrada.delete(0, tk.END)
    resultado.set("🔼 Nodo agregado\n" + mi_lista.mostrar())

def buscar_nodo():
    valor = entrada.get()
    if valor.strip() == "":
        return
    encontrado = mi_lista.buscar(valor)
    mensaje = f"🔍 {valor} {'encontrado ✅' if encontrado else 'no encontrado ❌'}"
    resultado.set(mensaje + "\n" + mi_lista.mostrar())

def eliminar_nodo():
    valor = entrada.get()
    if valor.strip() == "":
        return
    eliminado = mi_lista.eliminar(valor)
    mensaje = f"🗑️ {valor} {'eliminado ✅' if eliminado else 'no encontrado ❌'}"
    resultado.set(mensaje + "\n" + mi_lista.mostrar())

# Interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Lista Ligada Simple")
ventana.geometry("420x320")
ventana.config(bg="#f0f0f0")

tk.Label(ventana, text="Lista Ligada Simple", font=("Arial", 16), bg="#f0f0f0").pack(pady=10)

entrada = tk.Entry(ventana, width=30)
entrada.pack(pady=5)

# Botones
frame_botones = tk.Frame(ventana, bg="#f0f0f0")
frame_botones.pack()

tk.Button(frame_botones, text="Agregar", command=agregar_nodo, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5, pady=5)
tk.Button(frame_botones, text="Buscar", command=buscar_nodo, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5, pady=5)
tk.Button(frame_botones, text="Eliminar", command=eliminar_nodo, bg="#f44336", fg="white").grid(row=0, column=2, padx=5, pady=5)

resultado = tk.StringVar()
resultado.set("Lista: vacía")
tk.Label(ventana, textvariable=resultado, bg="#f0f0f0", font=("Courier", 11)).pack(pady=10)

ventana.mainloop()