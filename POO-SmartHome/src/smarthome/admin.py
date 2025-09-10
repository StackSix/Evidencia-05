from __future__ import annotations
from .usuario import Usuario, Email, USERS_DB

class Admin(Usuario):
    def __init__(self, nombre: str, email: Email):
        super().__init__(nombre=nombre, email=email, rol="admin")

    @classmethod
    def registrar_admin(cls, nombre: str, email: str, password: str) -> "Admin":
        if email in USERS_DB:
            raise ValueError("Ya existe un usuario con ese email.")
        a = cls(nombre=nombre, email=Email(email))
        a.establecer_password(password)
        USERS_DB[str(a.email)] = a._to_record()
        return a

    @classmethod
    def login_admin(cls, email: str, password: str) -> "Admin | None":
        u = Usuario.login(email, password)
        if u and u.rol == "admin":
            adm = cls(nombre=u.nombre, email=u.email)
            adm._password_hash = USERS_DB[email]["password_hash"]
            return adm
        return None
