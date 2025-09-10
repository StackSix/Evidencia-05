import pytest
from smarthome.admin import Admin
from smarthome.usuario import Usuario, USERS_DB

@pytest.fixture(autouse=True)
def limpiar_db():
    USERS_DB.clear()
    yield
    USERS_DB.clear()

def test_registro_admin_crea_usuario_con_rol_admin():
    a = Admin.registrar_admin("Root", "root@example.com", "admin123")
    assert a.rol == "admin"
    assert "root@example.com" in USERS_DB
    rec = USERS_DB["root@example.com"]
    assert rec["rol"] == "admin"
    assert "admin123" not in str(rec)  # nunca texto plano

def test_registro_admin_rechaza_email_duplicado():
    Admin.registrar_admin("Root", "root@example.com", "admin123")
    with pytest.raises(ValueError):
        Admin.registrar_admin("Otro", "root@example.com", "admin123")

def test_login_admin_ok_y_fallo():
    Admin.registrar_admin("Root", "root@example.com", "admin123")
    adm = Admin.login_admin("root@example.com", "admin123")
    assert isinstance(adm, Admin)
    assert adm.datos_publicos()["rol"] == "admin"

    # password incorrecta
    assert Admin.login_admin("root@example.com", "badpass") is None
    # usuario inexistente
    assert Admin.login_admin("no@example.com", "admin123") is None

def test_login_admin_no_debe_convertir_user_normal_en_admin():
    Usuario.registrar("User", "user@example.com", "userpass")
    # aunque haga login con email/password válidos, no es admin
    assert Admin.login_admin("user@example.com", "userpass") is None
