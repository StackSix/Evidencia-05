from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
from .usuario import Usuario, Email
from .exceptions import DuplicateError, NotFoundError

class IRepositorioUsuarios(ABC):
    @abstractmethod
    def guardar(self, usuario: Usuario) -> None: ...
    @abstractmethod
    def existe(self, email: str) -> bool: ...
    @abstractmethod
    def obtener(self, email: str) -> Usuario: ...

class RepositorioUsuariosEnMemoria(IRepositorioUsuarios):
    """
    Persistencia simple en memoria: un diccionario.
    Clave: email (str)
    Valor: dict serializado desde Usuario._datos_para_persistencia()
    """
    def __init__(self) -> None:
        self._db: Dict[str, dict] = {}

    def guardar(self, usuario: Usuario) -> None:
        key = str(usuario.email)
        if key in self._db:
            raise DuplicateError("El usuario ya existe.")
        self._db[key] = usuario._datos_para_persistencia()

    def existe(self, email: str) -> bool:
        return email in self._db

    def obtener(self, email: str) -> Usuario:
        data = self._db.get(email)
        if not data:
            raise NotFoundError("Usuario no encontrado.")
        return Usuario.desde_persistencia(data)

    # Utilidad para tests/demo
    def volcar_diccionario(self) -> dict:
        return dict(self._db)
