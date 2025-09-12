from __future__ import annotations
from .usuario import Usuario, Email, USERS_DB
from .exceptions import ValidationError 

class Admin(Usuario):
    def __init__(self, nombre: str, email: Email, permisos: bool = True):
        super().__init__(nombre=nombre, email=email, rol="admin")
        self._permisos = permisos

    @classmethod
    def registrar_admin(cls, nombre: str, email: str, password: str) -> "Admin":
        if email in USERS_DB:
            raise ValueError("Ya existe un usuario con ese email.")
        a = cls(nombre=nombre, email=Email(email))
        a.establecer_password(password)
        USERS_DB[email] = a._to_record()
        return a

    @classmethod
    def login_admin(cls, email: str, password: str) -> "Admin | None":
        u = Usuario.login(email, password)
        if u and u.rol == "admin":
            adm = cls(nombre=u.nombre, email=u.email)
            adm._password_hash = USERS_DB[email]["password_hash"]
            return adm
        return None

    def mostrar_automatizaciones_activas(self, repo_automatizaciones) -> str:
        activas = repo_automatizaciones.listar_activas()
        if not activas:
            return "No hay automatizaciones activas."
        return "\n".join(f"{a.id}: {a.nombre} ({a.tipo})" for a in activas)

    def agregar_dispositivo(self, repo_dispositivos, dispositivo, dueño_email: str) -> None:
        if not dueño_email:
            raise ValidationError("Dueño inválido.")
        repo_dispositivos.agregar(dispositivo, dueño_email)
        return None

    def eliminar_dispositivo(self, repo_dispositivos, device_id: int) -> None:
        repo_dispositivos.eliminar(device_id)
        return None

    def modificar_dispositivo(self, repo_dispositivos, device_id: int, **attrs) -> list:
        disp = repo_dispositivos.modificar(device_id, **attrs)
        return [f"{k}={getattr(disp, k)}" for k in attrs.keys()]

    def modificar_rol(self, repo_usuarios, email: str, nuevo_rol: str) -> list:
        user = repo_usuarios.obtener(email)
        anterior = user.rol
        user.modificar_rol(nuevo_rol)
        repo_usuarios.actualizar(user)
        return [email, anterior, nuevo_rol]
