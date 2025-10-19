from abc import ABC, abstractmethod
from typing import Optional, Any


class IDispositivoDAO(ABC):
    @abstractmethod
    def registrar_dispositivo(id_domicilio: Optional[int], id_tipo: int, etiqueta: str) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def obtener_dispositivo_usuario(self, identificador: Any) -> Optional[Any]:  
        raise NotImplementedError
    
    @abstractmethod
    def obtener_todos_dispositivos(id_domicilio: int) -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    def actualizar_dispositivo(self, entidad: Any) -> None:  
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_dispositivo(self, entidad: Any) -> None:  
        raise NotImplementedError