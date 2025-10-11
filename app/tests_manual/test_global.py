import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app.servicios.auth_service import AuthService
from app.dao.usuario_dao import UsuarioDAO
from app.dao.dispositivo_dao import DispositivoDAO
from app.dao.domicilio_dao import DomicilioDAO
from app.dao.tipo_habitacion_dao import TipoHabitacionDAO
from app.dao.automatizacion_dao import AutomatizacionDAO

print("=== 🔍 TEST GLOBAL SmartHome (Evidencia 6) ===")

# ---------------------------------------------
# 1️⃣ TEST: Crear un usuario
# ---------------------------------------------
try:
    nuevo_id = UsuarioDAO.crear_usuario(
        dni=55123456,
        id_rol=2,
        nombre="Test",
        apellido="User",
        email="test_user@example.com",
        contrasena="abc123"
    )
    print(f"✅ Usuario creado con ID {nuevo_id}")
except Exception as e:
    print(f"⚠️ No se pudo crear usuario: {e}")

# ---------------------------------------------
# 2️⃣ TEST: Agregar un domicilio
# ---------------------------------------------
try:
    nuevo_hogar = DomicilioDAO.crear_domicilio(
        direccion="Av. Siempre Viva",
        numeracion="742",
        ciudad="Cordoba",
        nombre_domicilio="Casa de Prueba"
    )
    print(f"✅ Domicilio creado con ID {nuevo_hogar}")
except Exception as e:
    print(f"⚠️ No se pudo crear domicilio: {e}")

# ---------------------------------------------
# 3️⃣ TEST: Agregar un dispositivo
# ---------------------------------------------
try:
    nuevo_disp = DispositivoDAO.crear_dispositivo(
        id_habitacion=1,
        id_tipo=1,
        estado=False,
        etiqueta="Cam Test"
    )
    print(f"✅ Dispositivo creado con ID {nuevo_disp}")
except Exception as e:
    print(f"⚠️ No se pudo crear dispositivo: {e}")

# ---------------------------------------------
# 4️⃣ TEST: Modificar contraseña (por admin)
# ---------------------------------------------
try:
    admin = {"rol": "admin"}
    AuthService.resetear_contrasena_admin(admin, email="test_user@example.com", nueva_contra="newpass123")
    print("✅ Contraseña actualizada correctamente.")
except Exception as e:
    print(f"⚠️ Error al cambiar contraseña: {e}")

# ---------------------------------------------
# 5️⃣ TEST: Crear automatización
# ---------------------------------------------
try:
    nueva_auto = AutomatizacionDAO.crear_automatizacion(
        id_hogar=1,
        nombre="Encender Luces Test",
        accion="ENCENDER_LUCES",
        dias="LU,MA,MI,JU,VI",
        hora="20:00",
        activa=True
    )
    print(f"✅ Automatización creada con ID {nueva_auto}")
except Exception as e:
    print(f"⚠️ No se pudo crear automatización: {e}")

# ---------------------------------------------
# 6️⃣ TEST: Cambiar nombre de habitación
# ---------------------------------------------
try:
    TipoHabitacionDAO.modificar_nombre(id_habitacion=1, nuevo_nombre="Living Smart")
    print("✅ Nombre de habitación modificado correctamente.")
except Exception as e:
    print(f"⚠️ No se pudo modificar habitación: {e}")

print("\n=== ✅ FIN DE PRUEBAS ===")
