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

# Campo: Desea ser contactado
tk.Label(formulario, text="¿Desea ser contactado? (No por los ovnis)", bg="#f2f2f2").grid(row=2, column=0, sticky="ne", padx=5, pady=5)
contacto_var = tk.BooleanVar(value=False)

tk.Radiobutton(formulario, text="Sí", variable=contacto_var, value=True, bg="#f2f2f2").grid(row=2, column=1, sticky="w")
tk.Radiobutton(formulario, text="No", variable=contacto_var, value=False, bg="#f2f2f2").grid(row=3, column=1, sticky="w")

# Campo: Tipo de sugerencia
tk.Label(formulario, text="Tipo de Mensaje", bg="#f2f2f2").grid(row=4, column=0, sticky="ne", padx=5, pady=5)

tipo_var = tk.StringVar(value="queja")

tk.Radiobutton(formulario, text="Queja", variable=tipo_var, value="queja", bg="#f2f2f2").grid(row=4, column=1, sticky="w")
tk.Radiobutton(formulario, text="Sugerencia", variable=tipo_var, value="sugerencia", bg="#f2f2f2").grid(row=5, column=1, sticky="w")
tk.Radiobutton(formulario, text="Felicitación", variable=tipo_var, value="felicitacion", bg="#f2f2f2").grid(row=6, column=1, sticky="w")

# Campo - Mensaje Largo
tk.Label(formulario, text="Mensaje", bg="#f2f2f2").grid(row=7, column=0, sticky="ne", padx=5, pady=5)
mensaje_text = tk.Text(formulario, width=30, height=5)
mensaje_text.grid(row=7, column=1, pady=5)

# Checkbutton de términos
acepta_terminos = tk.BooleanVar()
check_terminos = tk.Checkbutton(formulario, text="Acepto términos y condiciones", variable=acepta_terminos, bg="#f2f2f2")
check_terminos.grid(row=8, column=1, sticky="w", pady=10)

# Función para enviar formulario
def enviarFormulario():
    nombre = entrada_nombre.get().strip()
    correo = entrada_correo.get().strip()
    tipo = tipo_var.get()
    mensaje = mensaje_text.get("1.0", tk.END).strip()
    acepta = acepta_terminos.get()
    desea_contacto = contacto_var.get()

    # Validaciones básicas
    if not nombre or not mensaje:
        messagebox.showwarning("Campos incompletos", "Por favor completa los campos obligatorios")
        return
    
    # Validación de correo solo si desea ser contactado
    if desea_contacto:
        if not correo or "@" not in correo or "." not in correo:
            messagebox.showerror("Correo inválido", "Por favor ingresa un correo válido para ser contactado")
            return

    if not acepta:
        messagebox.showwarning("Términos no aceptados", "Debes aceptar los términos y condiciones")
        return
    
    # Si pasa todas las validaciones
    messagebox.showinfo("Formulario enviado!", f"Gracias por tu {tipo}, {nombre}")

    # Limpiar los campos
    entrada_nombre.delete(0, tk.END)
    entrada_correo.delete(0, tk.END)
    mensaje_text.delete("1.0", tk.END)
    tipo_var.set("queja")
    contacto_var.set("no")
    acepta_terminos.set(False)

# Botón de envío
boton_enviar = tk.Button(ventana, text="Enviar", command=enviarFormulario, bg="#4CAF50", fg="black", width=20)
boton_enviar.pack(pady=20)

ventana.mainloop()
