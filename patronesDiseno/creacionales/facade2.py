# me permite esconder complejidad detras de una interfaz sencilla
# tenemos una clase que interactua con muchas más
# simplificamos uso y reducimos acoplamiento
# es una "puerta de entrada al sistema" ABSTRACCION

# Analogía Cajero de Banco
# con simples llamdas y un par de botones puedes: depositar, retirar, sacar cheques, 
# cambiar el pin de la tarjeta etc etc

# Cuando usarlo
# cuando existe una complejidad enorme que se podría esconder detrás de una simple llamada
# cuando diseñamos las APIs
# cuando necesitamos un punto de acceso limpio

class Autenticador:
    def verificar_usuario(self, tarjeta, pin):
        print("✅ Verificando identidad del usuario...")
        # Enmascaramos una logica muy compleja aqui y en los demas
        return tarjeta == "1234-5678" and pin == "0000"

class BaseDeDatos:
    def __init__(self):
        self.saldo = 500

    def obtener_saldo(self):
        print("💰 Consultando saldo en la base de datos...")
        return self.saldo

    def actualizar_saldo(self, monto):
        print(f"💳 Actualizando saldo después del retiro de ${monto}...")
        self.saldo -= monto

class DispensadorEfectivo:
    def dispensar(self, monto):
        print(f"🤑 Dispensando ${monto} en efectivo...")

class ImpresoraRecibos:
    def imprimir(self, monto):
        print(f"🧾 Imprimiendo recibo por ${monto} retirados...")

# Clase Facade (la que oculta la complejidad)
class CajeroAutomatico:
    def __init__(self):
        self.autenticador = Autenticador()
        self.bd = BaseDeDatos()
        self.dispensador = DispensadorEfectivo()
        self.impresora = ImpresoraRecibos()

    def retirar_dinero(self, tarjeta, pin, monto):
        print("🔐 Iniciando operación de retiro...\n")
        
        if not self.autenticador.verificar_usuario(tarjeta, pin):
            print("🚫 Acceso denegado. Usuario o PIN incorrecto.")
            return

        saldo = self.bd.obtener_saldo()
        if monto > saldo:
            print("⚠️ Fondos insuficientes.")
            return

        self.dispensador.dispensar(monto)
        self.bd.actualizar_saldo(monto)
        self.impresora.imprimir(monto)
        print("\n✅ Operación completada exitosamente.")

# Crear instancia del CajeroFacade
cajero = CajeroAutomatico()

# Probar con tarjeta y pin correctos
cajero.retirar_dinero("1234-5678", "0000", 100)

# Probar con PIN incorrecto
cajero.retirar_dinero("1234-5678", "9999", 50)

# Probar con monto mayor al saldo
cajero.retirar_dinero("1234-5678", "0000", 1000) 