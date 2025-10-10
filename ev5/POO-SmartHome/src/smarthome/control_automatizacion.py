from abc import ABC, abstractmethod

class ControlAutomatizacion(ABC):
    """
    La Entidad ControlAutomatización es una Interfaz Formal, hereda de la clase base ABC.
    Es una clase Abstracta
    """
    @abstractmethod
    def configurar_automatizacion_horaria(self, on: str, off: str) -> str:
        pass
    
    @abstractmethod
    def mostrar_automatizacion(self) -> str:
        pass
