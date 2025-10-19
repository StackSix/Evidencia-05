from abc import ABC, abstractmethod
from typing import Optional, Any


class IUsuaioDAO(ABC):
    @abstractmethod

    def registrar_usuario(self, object):
        pass
    
    @abstractmethod
    def listar_todos_usuarios(self, identificador: Any) -> Optional[Any]:  
        raise NotImplementedError
    
    def obtener_por_email(email: str) -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    def actualizar_usuario(self, entidad: Any) -> None:  
        raise NotImplementedError
    
    @abstractmethod
    def modificar_rol(id_rol: int) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_usuario(self, entidad: Any) -> None:  
        raise NotImplementedError