# Nos permite encapsular una peticion (funcionalidad) como un objeto
# Guardamos un historial de acciones
# hacer y deshacer con el historial
# Ejecutamos acciones en diferido

# imaginemos una ORDEN enviada por el general (Avancen/ Ataquen / Retirense)
# El General no hace su orden (No la ejecuta), la envía en un papel
# A sus subordinados con un mensajero (COMMMAND)
# El mensajero se encarga que los subordinados ejecuten la accion

# Donde usarlo?
# cuando queremos que la app ejecute acciones de entrada (deeplinks)
# cuando queremos encadenar ejecuciones


class COMMAND:
    val tipo: String
    val value: String


class App:
    fun init__(COMMAND):
        if command == "deeplink"
            if value == "tiktok video"