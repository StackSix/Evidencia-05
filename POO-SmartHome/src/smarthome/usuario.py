# src/smarthome/usuario.py
from __future__ import annotations
import os, hmac, hashlib
from dataclasses import dataclass

# --- “Base de datos” en memoria ---
USERS_DB: dict[str, dict] = {}

# --- Seguridad / Hash ---
_ALGO = "pbkdf2"
_ITER = 120_000

def _pbkdf2(password: str, salt: bytes, iterations: int = _ITER) -> bytes:
    if not password:
        raise ValueError("La contraseña no puede ser vacía.")
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)

def _hash_password(password: str) -> str:
    if len(password) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres.")
    salt = os.urandom(16)
    digest = _pbkdf2(password, salt, _ITER)
    return f"{_ALGO}${_ITER}${salt.hex()}${digest.hex()}"

def _verify_password(password: str, stored: str) -> bool:
    try:
        algo, iter_str, salt_hex, hash_hex = stored.split("$", 3)
        if algo != _ALGO:
            return False
        iterations = int(iter_str)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
        got = _pbkdf2(password, salt, iterations)
        return hmac.compare_digest(got, expected)
    except Exception:
        return False

def _validar_email(email: str) -> None:
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Email inválido.")

# ---------- Value Object ----------
@dataclass(frozen=True)
class Email:
    direccion: str
    def __post_init__(self) -> None:
        _validar_email(self.direccion)
    def __str__(self) -> str:
        return self.direccion

# ---------- Entidad ----------
class Usuario:
    """
    Usuario con registro/login en memoria y contraseña hasheada.
    """
    def __init__(self, nombre: str, email: Email, rol: str = "user") -> None:
        if not nombre or len(nombre) < 2:
            raise ValueError("Nombre inválido.")
        self._nombre = nombre
        self._email = email
        self._rol = rol
        self._password_hash: str | None = None

    # ----- propiedades -----
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> Email:
        return self._email

    @property
    def rol(self) -> str:
        return self._rol

    # ----- helpers de persistencia -----
    def _to_record(self) -> dict:
        return {
            "nombre": self._nombre,
            "email": str(self._email),
            "rol": self._rol,
            "password_hash": self._password_hash,
        }

    @classmethod
    def _from_record(cls, rec: dict) -> "Usuario":
        u = cls(nombre=rec["nombre"], email=Email(rec["email"]), rol=rec.get("rol", "user"))
        u._password_hash = rec.get("password_hash")
        return u

    # ----- comportamiento -----
    def establecer_password(self, password_plano: str) -> None:
        self._password_hash = _hash_password(password_plano)

    def verificar_password(self, password_plano: str) -> bool:
        return bool(self._password_hash) and _verify_password(password_plano, self._password_hash)

    # ----- casos de uso -----
    @classmethod
    def registrar(cls, nombre: str, email: str, password: str, rol: str = "user") -> "Usuario":
        if email in USERS_DB:
            raise ValueError("Ya existe un usuario con ese email.")
        u = cls(nombre=nombre, email=Email(email), rol=rol)
        u.establecer_password(password)
        USERS_DB[email] = u._to_record()
        return u

    @classmethod
    def login(cls, email: str, password: str) -> "Usuario | None":
        rec = USERS_DB.get(email)
        if not rec:
            return None
        temp = cls._from_record(rec)
        if temp.verificar_password(password):
            return temp
        return None

    # para admin
    def cambiar_rol(self, nuevo: str) -> None:
        if not nuevo or len(nuevo) < 3:
            raise ValueError("Rol inválido.")
        self._rol = nuevo

    # vista segura
    def datos_publicos(self) -> dict:
        return {"nombre": self._nombre, "email": str(self._email), "rol": self._rol}
