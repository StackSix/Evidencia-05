import logging

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(logger=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class EventoDispositivo:
    """
    La Entidad EventoDispositivo representa un evento generado por un Dispositivo, como una Camara.
    Relación con class Camara: Agregación.
    Gestiona un id unico. 
    Envia notificaciones cuando un objeto Camara comienza o deja de grabar.
    """
    contador_id = 0
    def __init__(self) -> None:
        EventoDispositivo.contador_id +=1
        self.__evento_id: int = EventoDispositivo.contador_id
    
    @property
    def evento_id(self):
        return self.__evento_id
    
    # Comportamiento de la Clase
    def enviar_notificacion(self, evento: bool) -> str:
        mensaje = "El dispositivo comenzó grabar" if evento else "El dispositivo dejó grabar"
        logger.info(f"Evento ID: {self.evento_id}: {mensaje}")
        return mensaje
        