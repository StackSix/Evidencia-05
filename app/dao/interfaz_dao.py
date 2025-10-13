from abc import ABC, abstractmethod
from typing import Optional, Any


class DataAccessDAO(ABC):
    @abstractmethod

    def crear(self, object):
        pass
    
    @abstractmethod
    def leer(self, identificador: Any) -> Optional[Any]:  
        raise NotImplementedError
    
    @abstractmethod
    def actualizar(self, entidad: Any) -> None:  
        raise NotImplementedError
    
    @abstractmethod
    def eliminar(self, entidad: Any) -> None:  
        raise NotImplementedError
