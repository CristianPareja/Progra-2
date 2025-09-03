import tkinter as tk
from tkinter import messagebox

class Autenticador:
    def verificar_usuario(self, tarjeta, pin):
        print("Verificando identidad del usuario...")
        return tarjeta == "1234-5678" and pin == "0000"

class BaseDeDatos:
    def __init__(self):
        self.saldo = 500

    def obtener_saldo(self):
        print("Consultando saldo en la base de datos...")
        return self.saldo

    def actualizar_saldo(self, monto):
        print(f"Actualizando saldo después del retiro de ${monto}...")
        self.saldo -= monto

    def aumentar_saldo(self, monto):
        print(f"Aumentando saldo con un depósito de ${monto}...")
        self.saldo += monto

class DispensadorEfectivo:
    def dispensar(self, monto):
        print(f"Dispensando ${monto} en efectivo...")

class ImpresoraRecibos:
    def imprimir(self, monto):
        print(f"Imprimiendo recibo por ${monto} retirados...")


class CajeroAutomatico:
    def __init__(self):
        self.autenticador = Autenticador()
        self.bd = BaseDeDatos()
        self.dispensador = DispensadorEfectivo()
        self.impresora = ImpresoraRecibos()

    def retirar_dinero(self, tarjeta, pin, monto):
        print("Iniciando operación de retiro...\n")
        if not self.autenticador.verificar_usuario(tarjeta, pin):
            messagebox.showerror("Error", "Acceso denegado. Usuario o PIN incorrecto.")
            return

        saldo = self.bd.obtener_saldo()
        if monto > saldo:
            messagebox.showwarning("Fondos insuficientes", "No tiene suficiente saldo.")
            return

        self.dispensador.dispensar(monto)
        self.bd.actualizar_saldo(monto)
        self.impresora.imprimir(monto)
        messagebox.showinfo("Éxito", f"Se retiraron ${monto} exitosamente.")

    def depositar_dinero(self, tarjeta, pin, monto):
        print("Iniciando operación de depósito...\n")
        if not self.autenticador.verificar_usuario(tarjeta, pin):
            messagebox.showerror("Error", "Acceso denegado. Usuario o PIN incorrecto.")
            return

        self.bd.aumentar_saldo(monto)
        messagebox.showinfo("Depósito exitoso", f"Se depositaron ${monto} correctamente.")

    def consultar_saldo(self, tarjeta, pin):
        print("Iniciando consulta de saldo...\n")
        if not self.autenticador.verificar_usuario(tarjeta, pin):
            messagebox.showerror("Error", "Acceso denegado. Usuario o PIN incorrecto.")
            return

        saldo = self.bd.obtener_saldo()
        messagebox.showinfo("Saldo actual", f"Su saldo actual es: ${saldo}")

def ejecutar_operacion(operacion):
    tarjeta = entry_tarjeta.get()
    pin = entry_pin.get()
    monto_texto = entry_monto.get()

    if not tarjeta or not pin:
        messagebox.showerror("Error", "Tarjeta y PIN son obligatorios.")
        return

    monto = 0
    if monto_texto:
        try:
            monto = float(monto_texto)
            if monto < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Monto inválido.")
            return

    if operacion == "Retirar":
        cajero.retirar_dinero(tarjeta, pin, monto)
    elif operacion == "Depositar":
        cajero.depositar_dinero(tarjeta, pin, monto)
    elif operacion == "Consultar saldo":
        cajero.consultar_saldo(tarjeta, pin)

ventana = tk.Tk()
ventana.title("Cajero Automático")
ventana.geometry("320x250")

cajero = CajeroAutomatico()

tk.Label(ventana, text="Tarjeta:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_tarjeta = tk.Entry(ventana)
entry_tarjeta.grid(row=0, column=1)

tk.Label(ventana, text="PIN:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_pin = tk.Entry(ventana, show="*")
entry_pin.grid(row=1, column=1)

tk.Label(ventana, text="Monto:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_monto = tk.Entry(ventana)
entry_monto.grid(row=2, column=1)

# Botones
tk.Button(ventana, text=" Retirar", width=15, command=lambda: ejecutar_operacion("Retirar")).grid(row=3, column=0, pady=10)
tk.Button(ventana, text=" Depositar", width=15, command=lambda: ejecutar_operacion("Depositar")).grid(row=3, column=1)
tk.Button(ventana, text=" Consultar saldo", width=32, command=lambda: ejecutar_operacion("Consultar saldo")).grid(row=4, column=0, columnspan=2)

ventana.mainloop()
