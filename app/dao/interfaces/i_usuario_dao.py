from abc import ABC, abstractmethod
from typing import Optional, Any


class IUsuarioDAO(ABC):
    @abstractmethod
    def registrar_usuario(dni: int, nombre: str, apellido: str, email: str, contrasena: str, rol: str) -> int:
        pass
    
    @abstractmethod
    def listar_todos_usuarios() -> Optional[Any]: 
        raise NotImplementedError
    
    @abstractmethod
    def obtener_por_email(email: str) -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    def obtener_por_dni(dni: int) -> Optional[Any]:
        raise NotImplemented
    
    @abstractmethod
    def actualizar_usuario(id_usuario, email: str, nombre: str, apellido: str, contrasena: str) -> None:  
        raise NotImplementedError
    
    @abstractmethod
    def modificar_rol(id_usuario: int, nuevo_rol: str) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_usuario(id_usuario: int) -> None:  
        raise NotImplementedError
    