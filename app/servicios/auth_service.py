"""Servicios de autenticación basados en la base de datos en la nube."""
from __future__ import annotations
from typing import Dict, Optional
import bcrypt
from app.dao.usuarios_dao import UsuarioDAO

class AuthService:
    @staticmethod
    def registrar_usuario(
        dni: int,
        id_rol: int,
        nombre: str,
        apellido: str,
        email: str,
        contrasena: str,
    ) -> int:
        if len(contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        existente = UsuarioDAO.obtener_por_email(email)
        if existente:
            raise ValueError("Ya existe un usuario con ese email.")

        return UsuarioDAO.crear_usuario(dni, id_rol, nombre, apellido, email, contrasena)

    @staticmethod
    def login(email: str, contrasena_plana: str) -> Optional[Dict]:
        rec = UsuarioDAO.obtener_por_email(email)
        if not rec:
            return None
        hashed = rec.pop("contrasena", None)
        if not hashed or not bcrypt.checkpw(contrasena_plana.encode("utf-8"), hashed.encode("utf-8")):
            return None
        # fallback por si el DAO no trajo 'rol'
        if "rol" not in rec:
            rec["rol"] = "admin" if rec.get("id_rol") == 1 else "usuario"
        return rec

    @staticmethod
    def resetear_contrasena(email: str, dni: int, nueva_contra: str) -> bool:
        if len(nueva_contra) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        registro = UsuarioDAO.obtener_por_email(email)
        if not registro or registro.get("dni") != dni:
            return False

        # usa el alias que apunta a actualizar_contrasena_por_dni
        UsuarioDAO.actualizar_contrasena(dni, nueva_contra)
        return True

    @staticmethod
    def resetear_contrasena_admin(
        current_user: Dict,
        *,
        email: Optional[str] = None,
        dni: Optional[int] = None,
        nueva_contra: str,
    ) -> bool:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede resetear contraseñas.")
        if len(nueva_contra) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        if email is None and dni is None:
            raise ValueError("Debe indicar email o DNI del usuario a actualizar.")

        registro: Optional[Dict]
        if email is not None:
            registro = UsuarioDAO.obtener_por_email(email)
        else:
            registro = UsuarioDAO.obtener_por_dni(dni or 0)

        if not registro:
            return False

        UsuarioDAO.actualizar_contrasena_por_dni(registro["dni"], nueva_contra)
        return True