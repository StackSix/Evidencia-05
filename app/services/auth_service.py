# src/app/servicios/auth_service.py
from typing import Optional, Dict
import bcrypt
from app.dao.usuarios_dao import UsuarioDAO

class AuthService:
    @staticmethod
    def registrar_usuario(
        dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena: str, rol: str = "usuario"
    ) -> int:
        if len(contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        existente = UsuarioDAO.obtener_por_email(email)
        if existente:
            raise ValueError("Ya existe un usuario con ese email.")
        return UsuarioDAO.crear_usuario(dni, id_rol, nombre, apellido, email, contrasena, rol)

    @staticmethod
    def login(email: str, contrasena_plana: str) -> Optional[Dict]:
        rec = UsuarioDAO.obtener_por_email(email)
        if not rec:
            return None
        hashed = rec.pop("contrasena", None)
        if not hashed:
            return None
        ok = bcrypt.checkpw(contrasena_plana.encode("utf-8"), hashed.encode("utf-8"))
        return rec if ok else None

    @staticmethod
    def resetear_contrasena_admin(current_user: Dict, *, email: Optional[str]=None, dni: Optional[int]=None, nueva_contra: str="") -> bool:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede resetear contraseñas.")
        if not nueva_contra or len(nueva_contra) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        if email is None and dni is None:
            raise ValueError("Debe indicar email o dni del usuario a actualizar.")

        # localizar usuario por email o dni
        rec: Optional[Dict] = None
        if email:
            rec = UsuarioDAO.obtener_por_email(email)
        elif dni:
            rec = UsuarioDAO.obtener_por_dni(dni)

        if not rec:
            return False

        # usar DNI para el update (tu DAO actualiza por dni)
        UsuarioDAO.actualizar_contrasena(rec["dni"], nueva_contra)
        return True