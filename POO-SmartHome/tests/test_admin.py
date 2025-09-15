import pytest
from smarthome.admin import Admin
from smarthome.usuario import Usuario, USERS_DB

# ===================== Stubs locales (evitan imports faltantes) =====================

class Camara:
    def __init__(self, id: int, tipo: str, nombre: str, modelo: str, estado_dispositivo: str = "ON"):
        self.id = id
        self.tipo = tipo
        self.nombre = nombre
        self.modelo = modelo
        self.estado_dispositivo = estado_dispositivo

class RepositorioDispositivosEnMemoria:
    """
    Repo simple en memoria para dispositivos.
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

    def eliminar(self, device_id: int) -> None:
        if device_id not in self._dispositivos:
            raise ValueError(f"No existe el dispositivo #{device_id}.")
        self._dispositivos.pop(device_id, None)
        self._asignaciones.pop(device_id, None)

    def modificar(self, device_id: int, **attrs):
        disp = self._dispositivos.get(device_id)
        if not disp:
            raise ValueError(f"No existe el dispositivo #{device_id}.")
        for k, v in attrs.items():
            if not hasattr(disp, k):
                raise ValueError(f"Atributo inválido: {k}")
            setattr(disp, k, v)
        return disp

    def obtener(self, device_id: int):
        if device_id not in self._dispositivos:
            raise ValueError(f"No existe el dispositivo #{device_id}.")
        return self._dispositivos[device_id]

class Automatizacion:
    def __init__(self, id: int, nombre: str, tipo: str, activa: bool) -> None:
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.activa = activa

class RepositorioAutomatizacionesEnMemoria:
    """
    Repo mínimo de automatizaciones con filtro de activas.
    """
    def __init__(self) -> None:
        self._items = {}

    def agregar(self, auto: Automatizacion) -> None:
        if auto.id in self._items:
            raise ValueError("Automatización duplicada")
        self._items[auto.id] = auto

    def listar(self):
        return list(self._items.values())

    def listar_activas(self):
        return [a for a in self._items.values() if getattr(a, "activa", False)]

# =========================== Fixtures y helpers de test ============================

@pytest.fixture(autouse=True)
def limpiar_db():
    USERS_DB.clear()
    yield
    USERS_DB.clear()

def setup_context():
    # usuario normal
    Usuario.registrar("Daniel", "daniel@example.com", "secreto123")
    # admin
    admin = Admin.registrar_admin("Root", "root@example.com", "admin123")
    repo_disp = RepositorioDispositivosEnMemoria()
    repo_auto = RepositorioAutomatizacionesEnMemoria()
    return admin, repo_disp, repo_auto

# =================================== TESTS ===================================

def test_mostrar_automatizaciones_activas_devuelve_str():
    admin, _, repo_auto = setup_context()
    repo_auto.agregar(Automatizacion(id=201, nombre="Alerta Porch", tipo="MOTION_ALERT", activa=True))
    repo_auto.agregar(Automatizacion(id=202, nombre="Rutina Noche", tipo="SCHEDULE", activa=False))

    # Se asume que Admin.mostrar_automatizaciones_activas(repo) devuelve un str
    # con sólo las automatizaciones activas
    s = admin.mostrar_automatizaciones_activas(repo_auto)
    assert isinstance(s, str)
    assert "Alerta Porch" in s
    assert "Rutina Noche" not in s  # inactiva no debería aparecer

def test_agregar_y_eliminar_dispositivo_retorna_none_y_afecta_repo():
    admin, repo_disp, _ = setup_context()
    cam = Camara(id=101, tipo="CAMERA", nombre="Cam Porch", modelo="X1")

    # agregar_dispositivo(repo, dispositivo, owner_email) -> None
    ret = admin.agregar_dispositivo(repo_disp, cam, "daniel@example.com")
    assert ret is None
    assert repo_disp.obtener(101).nombre == "Cam Porch"

    # eliminar_dispositivo(repo, device_id) -> None
    ret = admin.eliminar_dispositivo(repo_disp, 101)
    assert ret is None
    with pytest.raises(Exception):
        repo_disp.obtener(101)
