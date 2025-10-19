from abc import ABC, abstractmethod
from typing import Optional, Any


class IAutomatizacionesDAO(ABC):
    @abstractmethod

    def registrar_automatizacion(self, object):
        pass
    
    @abstractmethod
    def obtener_automatizacion(self, identificador: Any) -> Optional[Any]:  
        raise NotImplementedError
    
    @abstractmethod
    def actualizar_automatizacion(self, entidad: Any) -> None:  
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_automatizacion(self, entidad: Any) -> None:  
        raise NotImplementedError