from abc import ABC, abstractmethod

class Dispositivo(ABC):
    "Clase para manejar dispositivos del hogar inteligente."

    def __init__(self, accion: str, id_dispositivo: int, id_habitacion: int, estado: str):
        self.accion = accion
        self.id_dispositivo = id_dispositivo
        self.id_habitacion = id_habitacion
        self.estado = estado

    def cambiar_estado(self, nuevo_estado: str):
        if nuevo_estado in ["encendido", "apagado"]: 
            self.estado = nuevo_estado
        else:
            raise ValueError("Estado no válido")

    def ejecutar_accion(self) -> str:
        return f"Dispositivo {self.id_dispositivo}: Acción genérica ejecutada."

    def detener_accion(self) -> str:
        return f"Dispositivo {self.id_dispositivo}: Acción genérica detenida."
    