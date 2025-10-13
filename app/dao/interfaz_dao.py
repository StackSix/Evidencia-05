from abc import ABC, abstractmethod
from typing import Optional

class DataAccessDAO(ABC):
    @abstractmethod

    def crear(self, object):
        pass
    
    @abstractmethod
    def leer(self, identificador: Any) -> Optional[Any]:  # pragma: no cover - interfaz
        raise NotImplementedError
    
    @abstractmethod
    def actualizar(self, entidad: Any) -> None:  # pragma: no cover - interfaz
        raise NotImplementedError
    
    @abstractmethod
    def eliminar(self, entidad: Any) -> None:  # pragma: no cover - interfaz
        raise NotImplementedError
