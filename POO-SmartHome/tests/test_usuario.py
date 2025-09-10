import re
import pytest
from smarthome.usuario import Usuario, Email, USERS_DB

@pytest.fixture(autouse=True)
def limpiar_db():
    USERS_DB.clear()
    yield
    USERS_DB.clear()

def test_registro_exitoso_guarda_en_diccionario_con_hash():
    u = Usuario.registrar("Daniel", "daniel@example.com", "secreto123")
    assert isinstance(u, Usuario)
    assert "daniel@example.com" in USERS_DB
    rec = USERS_DB["daniel@example.com"]
    # nunca texto plano
    assert "secreto123" not in str(rec)
    # formato hash esperado
    assert re.match(r"^pbkdf2\$\d+\$[0-9a-f]+\$[0-9a-f]+$", rec["password_hash"])

def test_registro_rechaza_email_duplicado():
    Usuario.registrar("Nahir", "nahir@example.com", "clave123")
    with pytest.raises(ValueError):
        Usuario.registrar("Otra", "nahir@example.com", "clave123")

def test_registro_rechaza_email_invalido():
    with pytest.raises(ValueError):
        Usuario.registrar("Agus", "correo-sin-arroba", "abcdef")

def test_registro_rechaza_password_corta():
    with pytest.raises(ValueError):
        Usuario.registrar("Gabi", "gabi@example.com", "123")

def test_login_exitoso_devuelve_usuario():
    Usuario.registrar("Sofi", "sofi@example.com", "mi_pass_99")
    u = Usuario.login("sofi@example.com", "mi_pass_99")
    assert isinstance(u, Usuario)
    assert u.datos_publicos() == {"nombre": "Sofi", "email": "sofi@example.com", "rol": "user"}

def test_login_falla_password_incorrecta_o_email_inexistente():
    Usuario.registrar("Jorge", "jorge@example.com", "StrongPass")
    assert Usuario.login("jorge@example.com", "otra") is None
    assert Usuario.login("noexiste@example.com", "StrongPass") is None

def test_email_value_object_valida_y_formatea():
    e = Email("ana@example.com")
    assert str(e) == "ana@example.com"
    with pytest.raises(ValueError):
        Email("ana@sinpunto")
