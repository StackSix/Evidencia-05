from abc import ABC, abstractmethod
from typing import Optional, Any


class IDomicilioDAO(ABC):
    @abstractmethod

    def registrar_domicilio(self, object):
        raise NotImplementedError
    
    @abstractmethod
    def obtener_domicilio_usuario(self, identificador: Any) -> Optional[Any]:  
        raise NotImplementedError
    
    @abstractmethod
    def actualizar_domicilio(self, entidad: Any) -> None:  
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_domicilio(self, entidad: Any) -> None:  
        raise NotImplementedError