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
    def ver_mis_datos(user_id: int, email_fallback: str | None = None) -> None:
        rec = UsuarioDAO.obtener_por_id(user_id)
        if not rec and email_fallback:
            # Fallback por si el id no matchea por algún motivo
            rec = UsuarioDAO.obtener_por_email(email_fallback)

        if not rec:
            print("⚠️  No se encontraron datos del usuario.")
            return

        rol_nombre = rec.get("rol") or "usuario"
        print("\n— Mis datos —")
        print(f"ID: {rec['id']}")
        print(f"DNI: {rec['dni']}")
        print(f"Nombre: {rec['nombre']} {rec['apellido']}")
        print(f"Email: {rec['email']}")
        print(f"Rol: {rol_nombre}")