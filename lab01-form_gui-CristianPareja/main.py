import tkinter as tk
from tkinter import messagebox, filedialog

# Ventana principal
ventana = tk.Tk()
ventana.title("Formulario de Saldo")
ventana.geometry("600x500")

#Entrada de datos y validaciones
def validar_datos():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    cedula = entry_cedula.get()
    saldo = entry_saldo.get()

    if not nombre or not correo or not cedula or not saldo:
        messagebox.showerror("Alerta", "Todos los campos son obligatorios")
        return
    
    if "@" not in correo or "." not in correo:
        messagebox.showerror("Alerta", "Correo electrónico inválido")
        return
    
    if not cedula.isdigit() or len(cedula) != 10:
        messagebox.showerror("Alerta", "Cédula inválida (debe tener 10 dígitos numéricos)")
        return
    
    try:
        saldo_float = float(saldo)
        if saldo_float < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Alerta", "Saldo inicial inválido (debe ser un número positivo)")
        return
    
    messagebox.showinfo("Éxito", f"Datos guardados correctamente:\nNombre: {nombre}\nCorreo: {correo}\nCédula: {cedula}\nSaldo: ${saldo_float:.2f}")

def exportar_txt():
    archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")])
    if archivo:
        with open(archivo, "w") as f:
            f.write(f"Nombre: {entry_nombre.get()}\n")
            f.write(f"Correo: {entry_correo.get()}\n")
            f.write(f"Cédula: {entry_cedula.get()}\n")
            f.write(f"Saldo inicial: {entry_saldo.get()}\n")
        messagebox.showinfo("Formulario exportado correctamente", f"Datos exportados a:\n{archivo}")

# Menú
menu = tk.Menu(ventana)
ventana.config(menu=menu)
archivo_menu = tk.Menu(menu)
archivo_menu.add_command(label="Exportar a TXT", command=exportar_txt)
menu.add_cascade(label="Archivo", menu=archivo_menu)

# Campos
tk.Label(ventana, text="Nombre:").pack(pady=5)
entry_nombre = tk.Entry(ventana, width=40)
entry_nombre.pack()

tk.Label(ventana, text="Correo:").pack(pady=5)
entry_correo = tk.Entry(ventana, width=40)
entry_correo.pack()

tk.Label(ventana, text="Cédula:").pack(pady=5)
entry_cedula = tk.Entry(ventana, width=40)
entry_cedula.pack()

tk.Label(ventana, text="Saldo inicial:").pack(pady=5)
entry_saldo = tk.Entry(ventana, width=40)
entry_saldo.pack()

tk.Button(ventana, text="Guardar", command=validar_datos, bg="#3498db", fg="white", width=20).pack(pady=15)

ventana.mainloop()
