import re
import pytest
from smarthome.usuario import Usuario, Email, USERS_DB

# --- Stubs locales para evitar dependencias externas que no existen aún ---

class Camara:
    def __init__(self, id: int, tipo: str, nombre: str, modelo: str, estado_dispositivo: str = "ON"):
        self.id = id
        self.tipo = tipo
        self.nombre = nombre
        self.modelo = modelo
        self.estado_dispositivo = estado_dispositivo

class RepositorioDispositivosEnMemoria:
    """
    Repo mínimo en memoria para probar Usuario.mostrar_dispositivos().
    Guarda (device_id -> dispositivo) y (device_id -> owner_email).
    """
    def __init__(self) -> None:
        self._dispositivos = {}
        self._asignaciones = {}

    def agregar(self, dispositivo, owner_email: str) -> None:
        if not hasattr(dispositivo, "id"):
            raise ValueError("El dispositivo debe tener atributo 'id'.")
        if dispositivo.id in self._dispositivos:
            raise ValueError("Dispositivo duplicado.")
        if not owner_email:
            raise ValueError("owner_email requerido.")
        self._dispositivos[dispositivo.id] = dispositivo
        self._asignaciones[dispositivo.id] = owner_email

    def listar_por_usuario(self, email: str):
        ids = [i for i, owner in self._asignaciones.items() if owner == email]
        return [self._dispositivos[i] for i in ids if i in self._dispositivos]

# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def limpiar_db():
    USERS_DB.clear()
    yield
    USERS_DB.clear()

def test_registro_exitoso_guarda_en_diccionario_con_hash():
    u = Usuario.registrar("Daniel", "daniel@example.com", "secreto123")
    assert isinstance(u, Usuario)
    rec = USERS_DB["daniel@example.com"]
    # no debe quedar la contraseña en texto plano
    assert "secreto123" not in str(rec)
    # formato pbkdf2$<iteraciones>$<salt_hex>$<hash_hex>
    assert re.match(r"^pbkdf2\$\d+\$[0-9a-f]+\$[0-9a-f]+$", rec["password_hash"])

def test_login_ok_y_fallo():
    Usuario.registrar("Sofi", "sofi@example.com", "mi_pass_99")
    # tu clase usa inicio_sesion en vez de login
    assert isinstance(Usuario.inicio_sesion("sofi@example.com", "mi_pass_99"), Usuario)
    assert Usuario.inicio_sesion("sofi@example.com", "pass_incorrecta") is None
    assert Usuario.inicio_sesion("no@existe.com", "loquesea") is None

def test_mostrar_datos_usuario_devuelve_str_legible():
    u = Usuario.registrar("Ana", "ana@example.com", "clave123")
    s = u.mostrar_datos_usuario()
    assert isinstance(s, str)
    assert "Ana" in s and "ana@example.com" in s and "user" in s

def test_mostrar_dispositivos_sin_repo_y_con_repo():
    u = Usuario.registrar("Luis", "luis@example.com", "clave123")
    # sin repo
    assert "repositorio" in u.mostrar_dispositivos().lower()

    # con repo y sin dispositivos
    repo = RepositorioDispositivosEnMemoria()
    assert "sin dispositivos" in u.mostrar_dispositivos(repo).lower()

    # agrego un dispositivo y debería listarlo
    cam = Camara(id=101, tipo="CAMERA", nombre="Cam Porch", modelo="X1")
    repo.agregar(cam, "luis@example.com")
    listado = u.mostrar_dispositivos(repo)
    assert "CAMERA#101" in listado and "Cam Porch" in listado
