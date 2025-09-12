from abc import ABC, abstractmethod

class ControlAutomatizacion(ABC):
    @abstractmethod
    def configurar_automatizacion_horaria():
        pass
    
    @abstractmethod
    def mostrar_automatizacion():
        pass
