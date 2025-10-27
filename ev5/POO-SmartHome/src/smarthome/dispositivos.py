import logging

# Configuración de logging: registra mensajes (info, advertencia, errores).
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format= "%(asctime)s [%(levelname)s] %(message)s")

class Dispositivo:
    """
    La Entidad Dispositivos es la clase base para cualquier dispositivos del sistema SmartHome.
    Gestiona un ID único.
    """
    _contador_id = 0
    def __init__(self, tipo, estado_dispositivo) -> None:
        Dispositivo._contador_id += 1
        self.__id: int = Dispositivo._contador_id
        self.__tipo: str = tipo
        self.__estado_dispositivo: str = estado_dispositivo
    
    # Propiedades
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def tipo(self) -> str:
        return self.__tipo
    
    @tipo.setter
    def tipo(self, nuevo_tipo):
        if not isinstance(nuevo_tipo, int):
            raise TypeError("El id debe ser un número entero.")
        self.__tipo = nuevo_tipo
    
    @property
    def estado_dispositivo(self) -> str:
        return self.__estado_dispositivo
    
    @estado_dispositivo.setter
    def estado_dispositivo(self, nuevo_estado):
        if nuevo_estado not in ["encendido", "apagado"]:
            raise ValueError("El estado no es válido. Debe ser 'encendido' o 'apagado'.")
        self.__estado_dispositivo = nuevo_estado
    
    # Método Mágico: mostra información        
    def __str__(self) -> str:
        return f'Datos del Dispositivo: \nID: {self.id} \nTipo: {self.tipo} \nEstado: {self.estado_dispositivo} \n'
    
    # Comportamiento
    def modificar_estado_dispositivo(self, nuevo_estado: str) -> str:
        if nuevo_estado not in ["encendido", "apagado"]:
            raise ValueError("Debe ingresar una opción válida segun el estado actual del dispositivo. Para ON: 'encendido' y para OFF: 'apagado'")
            
        self.__estado_dispositivo = nuevo_estado
        logger.info(f"{self.tipo} (ID {self.id}) cambiado a {self.__estado_dispositivo}")
        return self.__estado_dispositivo
    