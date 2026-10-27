"""Servicios de administración de usuarios apoyados en la base remota."""
from __future__ import annotations

from typing import Any, Dict, List

from app.dao.usuario_dao import UsuarioDAO


class UsuariosService:
    @staticmethod
    def listar() -> List[Dict[str, Any]]:
        usuarios = UsuarioDAO.obtener_todos()
        return [usuario.to_dict() for usuario in usuarios]

    @staticmethod
    def cambiar_rol_admin(current_user: Dict, usuario_id: int, nuevo_rol: str) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede cambiar roles.")

        rid = UsuarioDAO.obtener_id_rol_por_nombre(nuevo_rol)
        if rid is None:
            raise ValueError("Rol inexistente.")

        UsuarioDAO.cambiar_rol(usuario_id, rid)

    @staticmethod
    def eliminar_admin(current_user: Dict, dni: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede eliminar usuarios.")

        UsuarioDAO.eliminar(dni)
