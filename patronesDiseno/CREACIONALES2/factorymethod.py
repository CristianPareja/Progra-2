# Qué es?
# Delega la creacion de los objetos a las subclases, en lugar de crear las instancias directamente
# así desacoplamos la logica de creacion del objeto en si mismo

# Que problema resuelve
# cuando tenemos muchas clases que comparten la misma interfaz y necesitamos instanciar una u otra
# dependiendo el contexto, usamos if y let (esto rompe con el principio de OPEN/CLOSED de SOLID)

# Analogia
# Una pizzeria y su menu
# nosotros pedimos Pizza Napolitana y Pizza Hawaiiana; no sabemos como se hace pero al hacer el pedido la recibimos
# la pizzeria (cocina/fabrica) decide que pizza crear segun el contexto

# Cuando usarlo
# Cuando el tipo exacto de instancia no se conoce hasta ejecutar la aplicacion