#interfaces graficas en python
#todo lo que veamos en buenas practicas y configrucacion de codigo es aplicable a la ,ayoria de tecnologias
#intro y primeras ventanas con TKINTER

#Que es TKINTER?
#biblioteca estandar de python para crear interfaces graficas (GUI)
#biblioteca: es un codigo que ya hizo otra persona u organizacion que importamos para ser utilizado en nuestro proyecto (modulo, paquete, etc)

#verificacion si ya se puede importar una libreria
# try:
#     import tkinter as tk
#     print ("tkinter esta disponible")
# except ImportError:
#     print("tkinter no esta instalado. Instalalo")


# #empezamos con la primera ventana
# #importar la libreria y creamos una ventana basica

# import tkinter as tk

# #creamos una instancia de la ventana principal
# ventana = tk.Tk()

# #Cambiamos el titulo de la ventana
# ventana.title("Mi first python GUI")

# #definimos el tamano de la pantalla (anchoxalto)
# ventana.geometry("400x300")

# #mostramos la ventana y ejecutamos el main loop de eventos
# ventana.mainloop() #es un bucle que se ejcuta todo el tiempo esperando eventos

#Bloque 2: widgtes basicos y manejos de eventos

# import tkinter as tk
# ventana = tk.Tk()
# ventana.title("Widgets basicos en tkinter")
# ventana.geometry("1000x1000")
# ventana.configure(bg="#e6e6e6")

# #creamos un label (etiqueta)
# etiqueta = tk.Label(ventana, text="Mi primer label en Python", font=("Arial",16))
# #pack es las propiedades de label y entorno
# etiqueta.pack(pady=10)

# #creamos funcion para boton
# def saludar():
#     nombre = entrada_nombre.get() #obtener el texto del entry
#     etiqueta.config(text=f"Hola, {nombre}") #cambiamos el texto del label

# #definir el entry (campo de texto donde se ingresan datos)
# entrada_nombre = tk.Entry(ventana,bg="blue",fg="white",font=("Arial",14))
# entrada_nombre.pack(pady=10)

# #boton que llama a la funcion saludar
# boton_saludo=tk.Button(ventana,text="saludar", command=saludar, font=("Arial", 14))
# boton_saludo.pack(pady=10)
# #boton para cerrar la ventana
# boton_cerrar=tk.Button(ventana,text="Cerrar", command=ventana.destroy, fg="white", bg="red", font=("Arial", 12))
# boton_cerrar.pack(pady=10)
# ventana.mainloop()

# notas primer progreso 4 97,5 10

#bloque 3
# import tkinter as tk
# ventana = tk.Tk()
# ventana.title("Formulario de registro")
# ventana.geometry("450x300")
# ventana.configure(bg="#f2f2f2")

# #Frame para el formulario
# formulario=tk.Frame(ventana, bg="#f2f2f2", padx=20, pady=20)
# formulario.pack(pady=10)

# #etiquetas y campos
# tk.Label(formulario,text="Nombre", bg="#f2f2f2").grid(row=0, column=0, sticky="e",pady=5)

# entrada_nombre=tk.Entry(formulario,width=30)
# entrada_nombre.grid(row=0,column=1,pady=5)


# tk.Label(formulario,text="Apellido", bg="#f2f2f2").grid(row=1, column=0, sticky="e",pady=5)

# entrada_apellido=tk.Entry(formulario,width=30)
# entrada_apellido.grid(row=1,column=1,pady=5)


# tk.Label(formulario,text="Correo", bg="#f2f2f2").grid(row=2, column=0, sticky="e",pady=5)

# entrada_correo=tk.Entry(formulario,width=30)
# entrada_correo.grid(row=2,column=1,pady=5)

# #resultado
# resultado= tk.Label(formulario, text="", fg="green", bg="#f2f2f2", font=("Arial",12))
# resultado.grid(row=4, column=0, columnspan=2, pady=10)

# def registrar():
#     nombre=entrada_nombre.get()
#     apellido=entrada_apellido.get()
#     correo=entrada_correo.get()
    
#     if not nombre or not apellido or not correo:
#         resultado.config(text="todos los campos son obligatorios", fg="red")
#     elif "@" not in correo or "." not in correo:
#         resultado.config(text="correo invalido", fg="red")
#     else:
#         resultado.config(text=f"Bienvenido {nombre} {apellido}!", fg="green")

# #boton de accion para la funcion
# boton_registrar = tk.Button(formulario, text="Registrar", command=registrar, bg="#4CAf50", fg="white", width=20)
# boton_registrar.grid(row=3, column=0, columnspan=2, pady=10)

# ventana.mainloop()

#Ejercicio

# import tkinter as tk

# # Ventana principal
# ventana = tk.Tk()
# ventana.title("Calculadora de Densidad")
# ventana.geometry("450x300")
# ventana.configure(bg="#f2f2f2")

# # Frame para el formulario
# formulario = tk.Frame(ventana, bg="#f2f2f2", padx=20, pady=20)
# formulario.pack(pady=10)

# # Etiquetas y campos de entrada
# tk.Label(formulario, text="Masa (kg):", bg="#f2f2f2").grid(row=0, column=0, sticky="e", pady=5)
# entrada_masa = tk.Entry(formulario, width=30)
# entrada_masa.grid(row=0, column=1, pady=5)

# tk.Label(formulario, text="Volumen (m³):", bg="#f2f2f2").grid(row=1, column=0, sticky="e", pady=5)
# entrada_volumen = tk.Entry(formulario, width=30)
# entrada_volumen.grid(row=1, column=1, pady=5)

# # Resultado
# resultado = tk.Label(formulario, text="", fg="green", bg="#f2f2f2", font=("Arial", 12))
# resultado.grid(row=3, column=0, columnspan=2, pady=10)

# # Función para calcular la densidad
# def calcular_densidad():
#     try:
#         masa = float(entrada_masa.get())
#         volumen = float(entrada_volumen.get())

#         if masa <= 0 or volumen <= 0:
#             resultado.config(text="Masa y volumen deben ser mayores a 0", fg="red")
#         else:
#             densidad = masa / volumen
#             resultado.config(text=f"Densidad: {densidad:.2f} kg/m³", fg="green")
#     except ValueError:
#         resultado.config(text="Ingresa valores numéricos válidos", fg="red")

# # Botón para calcular
# boton_calcular = tk.Button(formulario, text="Calcular Densidad", command=calcular_densidad,
#                            bg="#4CAF50", fg="white", width=20)
# boton_calcular.grid(row=2, column=0, columnspan=2, pady=10)

# # Ejecutar ventana
# ventana.mainloop()

#challenge
import tkinter as tk

# Ventana principal
ventana = tk.Tk()
ventana.title("Formulario de cotización de autos")
ventana.geometry("800x700")
ventana.configure(bg="gray")

# Frame para el formulario
formulario = tk.Frame(ventana, bg="#f2f2f2", padx=20, pady=20)
formulario.pack(pady=10)

# Campos de entrada
tk.Label(formulario, text="Nombre:", bg="#f2f2f2").grid(row=0, column=0, sticky="e", pady=5)
entrada_nombre = tk.Entry(formulario, width=30)
entrada_nombre.grid(row=0, column=1, pady=5)

tk.Label(formulario, text="Apellido:", bg="#f2f2f2").grid(row=1, column=0, sticky="e", pady=5)
entrada_apellido = tk.Entry(formulario, width=30)
entrada_apellido.grid(row=1, column=1, pady=5)

tk.Label(formulario, text="Correo:", bg="#f2f2f2").grid(row=2, column=0, sticky="e", pady=5)
entrada_correo = tk.Entry(formulario, width=30)
entrada_correo.grid(row=2, column=1, pady=5)

tk.Label(formulario, text="Modelo del auto:", bg="#f2f2f2").grid(row=3, column=0, sticky="e", pady=5)
entrada_modelo = tk.Entry(formulario, width=30)
entrada_modelo.grid(row=3, column=1, pady=5)

tk.Label(formulario, text="Comentarios:", bg="#f2f2f2").grid(row=4, column=0, sticky="e", pady=5)
entrada_comentarios = tk.Text(formulario, width=30, height=4)
entrada_comentarios.grid(row=4, column=1, pady=5)

# Resultado
resultado = tk.Label(formulario, text="", fg="green", bg="#f2f2f2", font=("Arial", 12))
resultado.grid(row=6, column=0, columnspan=2, pady=10)

# Función para enviar la cotización
def cotizar():
    nombre = entrada_nombre.get()
    apellido = entrada_apellido.get()
    correo = entrada_correo.get()
    modelo = entrada_modelo.get()
    comentarios = entrada_comentarios.get("1.0", "end")
    
    if not nombre or not apellido or not correo or not modelo:
        resultado.config(text="Todos los campos son obligatorios", fg="red")
    elif "@" not in correo or "." not in correo:
        resultado.config(text="Correo inválido", fg="red")
    else:
        resultado.config(text=f"Gracias {nombre} {apellido}, recibirás tu cotización del modelo {modelo} al correo ingresado {correo}| Lugar y fecha de entrega {comentarios}", fg="green")

# Botón
boton_cotizar = tk.Button(formulario, text="Cotizar", command=cotizar, bg="#4CAF50", fg="white", width=20)
boton_cotizar.grid(row=5, column=0, columnspan=2, pady=10)

# Ejecutar ventana
ventana.mainloop()
