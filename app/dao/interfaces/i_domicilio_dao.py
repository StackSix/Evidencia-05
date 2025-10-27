from abc import ABC, abstractmethod
from typing import Optional, Any, List


class IDomicilioDAO(ABC):
    @abstractmethod
    def registrar_domicilio(direccion: str, ciudad: str, nombre_domicilio: str, id_usuario: int) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def obtener_domicilio_usuario(id_usuario: int) -> Optional[List[Any]]:  
        raise NotImplementedError
    
    @abstractmethod
    def obtener_todos_domicilios() -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    def actualizar_domicilio(id_domicilio: int, direccion: str, ciudad: str, nombre_domicilio: str) -> bool:  
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_domicilio(id_domicilio: int) -> bool:  
        raise NotImplementedError
    