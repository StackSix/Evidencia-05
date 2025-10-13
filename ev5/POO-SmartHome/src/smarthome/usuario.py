from __future__ import annotations
import os, hmac, hashlib
from dataclasses import dataclass

#
USERS_DB: dict[str, dict] = {}

_ALGO = "pbkdf2"
_ITER = 120_000



class Usuario:
    def __init__(self, nombre: str, email: str, rol: str = "user") -> None:
        if not nombre or len(nombre) < 2:
            raise ValueError("Nombre inválido.")
        self._nombre = nombre
        self._email = email
        self._rol = rol
        self._password_hash: str | None = None

    
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> str:
        return self._email

    @property
    def rol(self) -> str:
        return self._rol

    

    # ------------------ Métodos privados ------------------
    @staticmethod
    def _hash_contraseña(password: str, salt: bytes, iterations: int = _ITER) -> bytes:
        if not password:
            raise ValueError("La contraseña no puede ser vacía.")
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)

    @classmethod
    def _implementar_hash_contraseña(cls, password: str) -> str:
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        salt = os.urandom(16)
        digest = cls._hash_contraseña(password, salt, _ITER)
        return f"{_ALGO}${_ITER}${salt.hex()}${digest.hex()}"

    @classmethod
    def _verificar_contraseña(cls, password: str, stored: str) -> bool:
        try:
            algo, iter_str, salt_hex, hash_hex = stored.split("$", 3)
            if algo != _ALGO:
                return False
            iterations = int(iter_str)
            salt = bytes.fromhex(salt_hex)
            expected = bytes.fromhex(hash_hex)
            got = cls._hash_contraseña(password, salt, iterations)
            return hmac.compare_digest(got, expected)
        except Exception:
            return False

    @staticmethod
    def _validar_email(email: str) -> None:
        if not email or "@" not in email or "." not in email.split("@")[-1]:
            raise ValueError("Email inválido.")

    # ------------------ Métodos de instancia ------------------
    def establecer_password(self, password_plano: str) -> None:
        self._password_hash = self._implementar_hash_contraseña(password_plano)

    def verificar_password(self, password_plano: str) -> bool:
        return bool(self._password_hash) and self._verificar_contraseña(password_plano, self._password_hash)

    def mostrar_datos_usuario(self) -> str:
        return f"Usuario(nombre='{self._nombre}', email='{self._email}', rol='{self._rol}')"
    
    def almacenar_usuario_en_diccionario(self) -> dict:
        return {
            "nombre": self._nombre,
            "email": self._email,
            "rol": self._rol,
            "password_hash": self._password_hash,
        }

    # ------------------ Métodos de clase ------------------
    def almacenar_usuario_en_diccionario(self) -> dict:
        return {
            "nombre": self._nombre,
            "email": self._email,
            "rol": self._rol,
            "password_hash": self._password_hash,
        }

    @classmethod
    def traer_usuario_de_diccionario(cls, rec: dict) -> "Usuario":
        u = cls(nombre=rec["nombre"], email=rec["email"], rol=rec.get("rol", "user"))
        u._password_hash = rec.get("password_hash")
        return u

    @classmethod
    def registrar(cls, nombre: str, email: str, password: str, rol: str = "user") -> "Usuario":
        if email in USERS_DB:
            raise ValueError("Ya existe un usuario con ese email.")
        cls._validar_email(email)
        u = cls(nombre=nombre, email=email, rol=rol)
        u.establecer_password(password)
        USERS_DB[email] = u.almacenar_usuario_en_diccionario()
        return u

    @classmethod
    def inicio_sesion(cls, email: str, password: str) -> "Usuario | None":
        rec = USERS_DB.get(email)
        if not rec:
            return None
        temp = cls.traer_usuario_de_diccionario(rec)
        if temp.verificar_password(password):
            return temp
        return None

    def modificar_rol(self, nuevo: str) -> None:
        if not nuevo or len(nuevo) < 3:
            raise ValueError("Rol inválido.")
        self._rol = nuevo