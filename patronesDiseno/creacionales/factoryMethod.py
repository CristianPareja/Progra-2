# que es
# patron de diseno que se encarga de delegar la creacion de los objetos a las subclases, en lugar de creas instancias directamente, asi desacoplamos la logica de creacion
# del objeto en si mismo.
#que pronlema resuelve
# cuando tenermos muchas clases que comparten la misma interfaz y necesitamos instancia una u otra depndiendo el contexto
#usamos if y let (esto rompe con el principio de OPEN/CLOSED de SOLID)

#Analogia
#Pizeria y su menu
#nosotros pedimos pizza napolitana y pizza hawaiana: no sabemos como se hace pero al hacer el pedido la recibimos.
# la pcocina decide que pizza crear segun el contexto

#Cuando usarlo
# Cuando el tipo exacto de instancia no se conoce hasta ejecutar la aplicacion. cuando hay una sola interfaz pero varios subtipos

#definimos la clase base/abstracta o interfaz con el comportamiento comun
class Notification:
    def enviar(self, mensaje):
        raise NotImplementedError("Este método debe ser implementado por las clases concretas")

# Clases concretas que implementan la interfaz
class NotificationEmail(Notification):
    def enviar(self, mensaje):
        print(f"Enviando mensaje por email: {mensaje}")

class NotificationSMS(Notification):
    def enviar(self, mensaje):
        print(f"Enviando mensaje por SMS: {mensaje}")

# Fábrica de notificaciones
class NotificationFactory:
    def crear_notification(self, tipo):
        if tipo == "email":
            return NotificationEmail()
        elif tipo == "sms":
            return NotificationSMS()
        else:
            raise ValueError("Tipo de notificación no soportado")

# Creamos la fábrica
factory = NotificationFactory()

# Obtenemos el objeto deseado usando la fábrica y enviamos el mensaje
notificacion_sms = factory.crear_notification("sms")
notificacion_sms.enviar("Tu código de confirmación es 1234")

notificacion_email = factory.crear_notification("email")
notificacion_email.enviar("¡Días PUCE, no te lo pierdas!")
