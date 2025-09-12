import pytest
from smarthome.admin import Admin
from smarthome.usuario import Usuario, Email, USERS_DB
from smarthome.repositorio_usuarios import RepositorioUsuariosEnMemoria
from smarthome.repositorio_dispositivos import RepositorioDispositivosEnMemoria
from smarthome.automatizaciones import RepositorioAutomatizacionesEnMemoria, Automatizacion
from smarthome.camara import Camara

@pytest.fixture(autouse=True)
def limpiar_db():
    USERS_DB.clear()
    yield
    USERS_DB.clear()

def setup_context():
    repo_users = RepositorioUsuariosEnMemoria()
    # usuario normal
    Usuario.registrar("Daniel", "daniel@example.com", "secreto123")
    # admin
    admin = Admin.registrar_admin("Root", "root@example.com", "admin123")
    repo_disp = RepositorioDispositivosEnMemoria()
    repo_auto = RepositorioAutomatizacionesEnMemoria()
    return admin, repo_users, repo_disp, repo_auto

def test_mostrar_automatizaciones_activas_devuelve_str():
    admin, _, _, repo_auto = setup_context()
    repo_auto.agregar(Automatizacion(id=201, nombre="Alerta Porch", tipo="MOTION_ALERT", activa=True))
    repo_auto.agregar(Automatizacion(id=202, nombre="Rutina Noche", tipo="SCHEDULE", activa=False))
    s = admin.mostrar_automatizaciones_activas(repo_auto)
    assert isinstance(s, str)
    assert "Alerta Porch" in s
    assert "Rutina Noche" not in s  # inactiva no debería aparecer

def test_agregar_y_eliminar_dispositivo_retorna_none_y_afecta_repo():
    admin, _, repo_disp, _ = setup_context()
    cam = Camara(id=101, tipo="CAMERA", nombre="Cam Porch", modelo="X1")

    # agregar_dispositivo(): None
    ret = admin.agregar_dispositivo(repo_disp, cam, "daniel@example.com")
    assert ret is None
    assert repo_disp.obtener(101).nombre == "Cam Porch"

    # eliminar_dispositivo(): None
    ret = admin.eliminar_dispositivo(repo_disp, 101)
    assert ret is None
    with pytest.raises(Exception):
        repo_disp.obtener(101)

def test_modificar_dispositivo_devuelve_lista_de_cambios():
    admin, _, repo_disp, _ = setup_context()
    cam = Camara(id=102, tipo="CAMERA", nombre="Cam Vieja", modelo="X1")
    repo_disp.agregar(cam, "daniel@example.com")

    cambios = admin.modificar_dispositivo(repo_disp, 102, nombre="Cam Nueva", estado_dispositivo="ON")
    assert isinstance(cambios, list)
    assert "nombre=Cam Nueva" in cambios and "estado_dispositivo=ON" in cambios

def test_modificar_rol_devuelve_lista_informativa():
    admin, repo_users, *_ = setup_context()
    # sincronizar el usuario en el repo de usuarios en memoria (guardar)
    u = Usuario.login("daniel@example.com", "secreto123")
    repo_users.guardar(u)

    res = admin.modificar_rol(repo_users, "daniel@example.com", "manager")
    assert res == ["daniel@example.com", "user", "manager"]
