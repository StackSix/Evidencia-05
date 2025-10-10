# src/smarthome/admin.py
from __future__ import annotations
from .usuario import Usuario, Email, USERS_DB

class Admin(Usuario):
    def __init__(self, nombre: str, email: Email):
        # Forzamos el rol "admin"
        super().__init__(nombre=nombre, email=email, rol="admin")

    # ---------- Casos de uso ----------
    @classmethod
    def registrar_admin(cls, nombre: str, email: str, password: str) -> "Admin":
        if email in USERS_DB:
            raise ValueError("Ya existe un usuario con ese email.")
        a = cls(nombre=nombre, email=Email(email))
        a.establecer_password(password)
        # En tu Usuario el método se llama almacenar_usuario_en_diccionario
        USERS_DB[email] = a.almacenar_usuario_en_diccionario()
        return a

    @classmethod
    def login_admin(cls, email: str, password: str) -> "Admin | None":
        # Tu Usuario usa 'inicio_sesion' en vez de 'login'
        u = Usuario.inicio_sesion(email, password)
        if u and u.rol == "admin":
            adm = cls(nombre=u.nombre, email=u.email)
            # preservamos el hash que está en USERS_DB
            rec = USERS_DB.get(email, {})
            adm._password_hash = rec.get("password_hash")
            return adm
        return None

    # ---------- Funciones pedidas por tests ----------
    def mostrar_automatizaciones_activas(self, repo_automatizaciones) -> str:
        """
        Debe listar solo las automatizaciones activas.
        Se espera que 'repo_automatizaciones' tenga listar_activas() -> list[Automatizacion]
        """
        if repo_automatizaciones is None or not hasattr(repo_automatizaciones, "listar_activas"):
            return "No hay repositorio de automatizaciones disponible."
        activas = repo_automatizaciones.listar_activas()
        if not activas:
            return "Sin automatizaciones activas."
        # Formato simple: "id - nombre (tipo)" por línea
        return "\n".join(f"{a.id} - {a.nombre} ({a.tipo})" for a in activas)

    def agregar_dispositivo(self, repo_dispositivos, dispositivo, owner_email) -> None:
        """
        Debe delegar en repo_dispositivos.agregar(dispositivo, owner_email)
        """
        if repo_dispositivos is None or not hasattr(repo_dispositivos, "agregar"):
            raise ValueError("Repositorio de dispositivos inválido.")
        repo_dispositivos.agregar(dispositivo, owner_email)

    def eliminar_dispositivo(self, repo_dispositivos, device_id: int) -> None:
        """
        Debe delegar en repo_dispositivos.eliminar(device_id)
        """
        if repo_dispositivos is None or not hasattr(repo_dispositivos, "eliminar"):
            raise ValueError("Repositorio de dispositivos inválido.")
        repo_dispositivos.eliminar(device_id)
