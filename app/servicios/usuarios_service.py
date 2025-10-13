"""Servicios de administración de usuarios apoyados en la base remota."""
from __future__ import annotations
from typing import Dict, List
from app.dao.usuarios_dao import UsuarioDAO

class UsuariosService:
    @staticmethod
    def listar() -> List[Dict]:
        return UsuarioDAO.obtener_todos()

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

    @staticmethod
    def ver_mis_datos(dni: int) -> None:
        u = UsuarioDAO.obtener_por_dni(dni)
        if not u:
            print("⚠️  No se encontraron datos del usuario.")
            return
        # si querés el nombre del rol, lo traes aparte o añadís join en obtener_por_dni
        print("\n— Mis datos —")
        print(f"ID: {u['id']}")
        print(f"DNI: {u['dni']}")
        print(f"Nombre: {u['nombre']} {u['apellido']}")
        print(f"Email: {u['email']}")
        # opcional: rol_nombre si lo agregas al SELECT
        if 'rol_nombre' in u:
            print(f"Rol: {u['rol_nombre']}")