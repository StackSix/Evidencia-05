# src/app/servicios/auth_service.py
from typing import Optional, Dict
import bcrypt
from app.dao.usuario_dao import UsuarioDAO

class AuthService:
    @staticmethod
    def registrar_usuario(
        dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena: str, rol: str = "usuario"
    ) -> int:
        # regla de negocio: contraseñas mínimas 6
        if len(contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        # evita duplicado por email
        existente = UsuarioDAO.obtener_por_email(email)
        if existente:
            raise ValueError("Ya existe un usuario con ese email.")
        return UsuarioDAO.crear_usuario(dni, id_rol, nombre, apellido, email, contrasena, rol)

    @staticmethod
    def login(email: str, contrasena_plana: str) -> Optional[Dict]:
        """Devuelve un dict de usuario (sin hash) si ok; None si falla."""
        rec = UsuarioDAO.obtener_por_email(email)
        if not rec:
            return None
        hashed = rec.pop("contrasena", None)  # alias que definimos en el DAO
        if not hashed:
            return None
        ok = bcrypt.checkpw(contrasena_plana.encode("utf-8"), hashed.encode("utf-8"))
        return rec if ok else None

    @staticmethod
    def resetear_contrasena(email: str, dni: int, nueva_contra: str) -> bool:
        """Flujo simple: valida identidad por email + DNI y setea nueva contraseña."""
        if len(nueva_contra) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        rec = UsuarioDAO.obtener_por_email(email)
        if not rec:  # no existe
            return False
        if rec.get("dni") != dni:  # identidad no coincide
            return False
        UsuarioDAO.actualizar_contrasena(dni, nueva_contra)
        return True
