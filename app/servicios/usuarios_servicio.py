# src/app/servicios/usuarios_service.py
from typing import List, Dict
from app.dao.usuario_dao import UsuarioDAO

class UsuariosService:
    @staticmethod
    def listar() -> List[Dict]:
        return UsuarioDAO.obtener_todos()

    @staticmethod
    def cambiar_rol_admin(current_user: Dict, user_id: int, nuevo_rol: str) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede cambiar roles.")
        rid = UsuarioDAO.obtener_id_rol_por_nombre(nuevo_rol)
        if rid is None:
            raise ValueError("Rol inexistente.")
        UsuarioDAO.cambiar_rol(user_id, rid)

    @staticmethod
    def eliminar_admin(current_user: Dict, dni: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede eliminar usuarios.")
        UsuarioDAO.eliminar(dni)
