import re
import pytest
from smarthome.usuario import Usuario, Email, USERS_DB
from smarthome.repositorio_dispositivos import RepositorioDispositivosEnMemoria
from smarthome.camara import Camara

@pytest.fixture(autouse=True)
def limpiar_db():
    USERS_DB.clear()
    yield
    USERS_DB.clear()

def test_registro_exitoso_guarda_en_diccionario_con_hash():
    u = Usuario.registrar("Daniel", "daniel@example.com", "secreto123")
    assert isinstance(u, Usuario)
    rec = USERS_DB["daniel@example.com"]
    assert "secreto123" not in str(rec)
    assert re.match(r"^pbkdf2\$\d+\$[0-9a-f]+\$[0-9a-f]+$", rec["password_hash"])

def test_login_ok_y_fallo():
    Usuario.registrar("Sofi", "sofi@example.com", "mi_pass_99")
    assert isinstance(Usuario.login("sofi@example.com", "mi_pass_99"), Usuario)
    assert Usuario.login("sofi@example.com", "pass_incorrecta") is None
    assert Usuario.login("no@existe.com", "loquesea") is None

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
