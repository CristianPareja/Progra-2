import tkinter as tk
from tkinter import messagebox
# Creamos la ventana principal
ventana = tk.Tk()
ventana.title("Formulario de sugerencias")
ventana.geometry("500x500")
ventana.configure(bg="#f2f2f2")
# Titulo principal
titulo = tk.Label(ventana, text="Formulario de sugerencias")
titulo.pack(pady=10)
# Frame para agrupar elementos principales
formulario = tk.Frame(ventana, bg="#f2f2f2")
formulario.pack(pady=10)
# Campo nombre
tk.Label(formulario, text="Nombre:", bg="#f2f2f2").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entrada_nombre = tk.Entry(formulario, width=40)
entrada_nombre.grid(row=0, column=1, pady=5)
# Campo Correo
tk.Label(formulario, text="Correo:", bg="#f2f2f2").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entrada_correo = tk.Entry(formulario, width=40)
entrada_correo.grid(row=1, column=1, pady=5)
## sticky define hacia que direccion está alineado un widget
# w - alineado a la izquierda (west)
# e - alineado a la derecha (east)
# n - alineado hacia arriba (north)
# s - alineado hacia abajo (south)
# pueden ser combinables
# ns expandido de arriba hacia abajo
# en alineado de derecha y arriba
# nsew expandido hacia todos sus lados
tk.Label(ventana, text="Izquierda").grid(row=0, column=0, sticky="w")
tk.Label(ventana, text="Derecha").grid(row=1, column=0, sticky="e")
tk.Label(ventana, text="arriba").grid(row=2, column=0, sticky="n")
tk.Label(ventana, text="Relleno completo").grid(row=3, column=0, sticky="nsew")


