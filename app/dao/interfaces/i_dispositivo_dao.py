from abc import ABC, abstractmethod
from typing import Optional, Any


class IDispositivoDAO(ABC):
    @abstractmethod
    def registrar_dispositivo(id_domicilio: Optional[int], id_tipo: int, estado: str, etiqueta: str) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def obtener_dispositivo_usuario(id_usuario: int) -> Optional[Any]:  
        raise NotImplementedError
    
    @abstractmethod
    def obtener_todos_dispositivos() -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    def listar_dispositivos_por_domicilio(id_domicilio: int) -> Optional[Any]:
        raise NotImplementedError
        
    @abstractmethod
    def actualizar_dispositivo(id_dispositivo: int, *, id_domicilio: Optional[int] = None, id_tipo: Optional[int] = None, estado: Optional[str] = None, etiqueta: Optional[str] = None) -> None:  
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_dispositivo(id_dispositivo: int) -> None:  
        raise NotImplementedError
    
    