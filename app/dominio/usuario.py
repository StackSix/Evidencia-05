"""Modelo de dominio para representar usuarios."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Mapping, Optional


@dataclass(frozen=True)
class Usuario:
    """Entidad de usuario utilizada en la capa de dominio."""

    id: Optional[int]
    dni: int
    id_rol: int
    nombre: str
    apellido: str
    email: str
    rol: Optional[str] = None
    contrasena: Optional[str] = None

    @classmethod
    def desde_fila(cls, fila: Mapping[str, Any]) -> "Usuario":
        """Construye una instancia a partir de una fila proveniente de la BD."""

        return cls(
            id=fila.get("id"),
            dni=int(fila["dni"]),
            id_rol=int(fila["id_rol"]),
            nombre=str(fila["nombre"]),
            apellido=str(fila["apellido"]),
            email=str(fila["email"]),
            rol=fila.get("rol"),
            contrasena=fila.get("contrasena"),
        )

    def to_dict(self, *, incluir_contrasena: bool = False) -> Dict[str, Any]:
        """Devuelve un diccionario serializable del usuario."""

        data: Dict[str, Any] = {
            "id": self.id,
            "dni": self.dni,
            "id_rol": self.id_rol,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "rol": self.rol,
        }
        if incluir_contrasena and self.contrasena is not None:
            data["contrasena"] = self.contrasena
        return data

    def sin_contrasena(self) -> Dict[str, Any]:
        """Atajo para obtener la representación sin el hash de la contraseña."""

        return self.to_dict(incluir_contrasena=False)
