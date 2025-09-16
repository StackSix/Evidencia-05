from __future__ import annotations
import getpass
import sys

from .usuario import Usuario, USERS_DB
from .admin import Admin

try:
    from smarthome.usuario import Usuario, USERS_DB
    from smarthome.admin import Admin
    from smarthome.menu_config_dispositivos import menu_dispositivo
    from smarthome.camara import Camara, ModoGrabacion
except ImportError:
    from .usuario import Usuario, USERS_DB
    from .admin import Admin
    from .menu_config_dispositivos import menu_dispositivo
    from .camara import Camara, ModoGrabacion

try:
    from .menu_config_dispositivos import menu_dispositivo  
except Exception:
    from menu_config_dispositivos import menu_dispositivo 

try:
    from .camara import Camara, ModoGrabacion
except Exception:
    from camara import Camara, ModoGrabacion 

class RepoDispositivosMem:
    def __init__(self) -> None:
        self._disps: dict[int, object] = {}
        self._owners: dict[int, str] = {}

    def agregar(self, dispositivo, owner_email: str) -> None:
        if not hasattr(dispositivo, "id"):
            raise ValueError("El dispositivo debe tener atributo 'id'.")
        self._disps[dispositivo.id] = dispositivo
        self._owners[dispositivo.id] = owner_email

    def listar_por_usuario(self, email: str):
        ids = [i for i, o in self._owners.items() if o == email]
        return [self._disps[i] for i in ids if i in self._disps]

    def obtener(self, device_id: int):
        return self._disps[device_id]

    def eliminar(self, device_id: int) -> None:
        self._disps.pop(device_id, None)
        self._owners.pop(device_id, None)


repo_disps = RepoDispositivosMem()


def pedir_opcion(prompt: str, validas: set[str]) -> str:
    while True:
        op = input(prompt).strip()
        if op in validas:
            return op
        print("Opción inválida.")

def pedir_email() -> str:
    while True:
        e = input("Email: ").strip()
        if "@" in e and "." in e.split("@")[-1]:
            return e
        print("Email inválido.")

def pedir_nombre() -> str:
    while True:
        n = input("Nombre: ").strip()
        if len(n) >= 2:
            return n
        print("Nombre inválido (mín. 2 caracteres).")

def pedir_password() -> str:
    while True:
        p = getpass.getpass("Contraseña: ").strip()
        if len(p) >= 6:
            return p
        print("La contraseña debe tener al menos 6 caracteres.")


def construir_camara_por_defecto() -> Camara | None:
    """
    Tu Camara tiene firma:
      Camara(tipo, estado_dispositivo, nombre, modelo, ModoGrabacion, modo_grabando, estado_automatizacion)
    """
    try:
        cam = Camara("camara", "encendido", "Cam-Default", "M1", ModoGrabacion.MANUAL, False, False)
       
        if not hasattr(cam, "id"):
            setattr(cam, "id", 101)
        return cam
    except Exception as e:
        print("[WARN] No pude construir cámara por defecto:", e, file=sys.stderr)
        return None

def asegurar_dispositivo_para(email: str):
    dispositivos = repo_disps.listar_por_usuario(email)
    if dispositivos:
        return dispositivos
    cam = construir_camara_por_defecto()
    if cam:
        repo_disps.agregar(cam, email)
        dispositivos = repo_disps.listar_por_usuario(email)
    return dispositivos


def menu_admin(admin: Admin):
    while True:
        print("\n=== MENÚ ADMIN ===")
        print("1) Ver usuarios")
        print("2) Cambiar rol de usuario (user/admin)")
        print("3) Ir a menú de dispositivo")
        print("4) Agregar dispositivo a un usuario")
        print("5) Eliminar dispositivo de un usuario")
        print("6) Cerrar sesión")
        op = pedir_opcion("Elegí una opción: ", {"1", "2", "3", "4","5","6"})

        if op == "1":
            if not USERS_DB:
                print("No hay usuarios registrados.")
            else:
                for email, data in USERS_DB.items():
                    print(f"- {data['nombre']} <{email}>  rol={data['rol']}")
        elif op == "2":
            email = pedir_email()
            if email not in USERS_DB:
                print("No existe ese usuario.")
                continue
            nuevo = input("Nuevo rol (user/admin): ").strip().lower()
            if nuevo not in ("user", "admin"):
                print("Rol inválido.")
                continue
            u = Usuario.traer_usuario_de_diccionario(USERS_DB[email])
            try:
                u.modificar_rol(nuevo)
                USERS_DB[email] = u.almacenar_usuario_en_diccionario()
                print("✅ Rol actualizado.")
            except Exception as e:
                print("Error al actualizar rol:", e)
        elif op == "3":
            dispositivos = asegurar_dispositivo_para(str(admin.email))
            if not dispositivos:
                print("No hay dispositivos disponibles.")
                continue
            cam = dispositivos[0]
            print(f"\n→ Entrando a configuración de: {getattr(cam, 'nombre', 'Cámara')}")
            menu_dispositivo(cam)
        elif op == "4":
            # Agregar dispositivo a usuario
            email = pedir_email()
            if email not in USERS_DB:
                print("No existe ese usuario.")
                continue
            cam = construir_camara_por_defecto()
            if cam:
                repo_disps.agregar(cam, email)
                print(f"✅ Dispositivo {cam.nombre} agregado a {email}.")
        elif op == "5":
            # Eliminar dispositivo de usuario
            email = pedir_email()
            dispositivos = repo_disps.listar_por_usuario(email)
            if not dispositivos:
                print("Este usuario no tiene dispositivos.")
                continue
            print("Dispositivos del usuario:")
            for d in dispositivos:
                print(f"- ID: {d.id}, Nombre: {getattr(d, 'nombre', 'Desconocido')}")
            device_id = int(input("Ingresá el ID del dispositivo a eliminar: "))
            repo_disps.eliminar(device_id)
            print("✅ Dispositivo eliminado.")
        elif op == "6":
            print("👋 Sesión cerrada.")
            return


def menu_usuario(usuario: Usuario):
    while True:
        print("\n=== MENÚ USUARIO ===")
        print("1) Ver mis datos")
        print("2) Ir a menú de dispositivo")
        print("3) Cerrar sesión")
        op = pedir_opcion("Elegí una opción: ", {"1", "2", "3"})

        if op == "1":
            print(usuario.mostrar_datos_usuario())
        elif op == "2":
            dispositivos = asegurar_dispositivo_para(str(usuario.email))
            if not dispositivos:
                print("No tenés dispositivos asignados.")
                continue
            cam = dispositivos[0]
            print(f"\n→ Entrando a configuración de: {getattr(cam, 'nombre', 'Cámara')}")
            menu_dispositivo(cam)
        elif op == "3":
            print("👋 Sesión cerrada.")
            return


def menu_auth():
    while True:
        print("\n=== SmartHome Auth ===")
        print("1) Registrarse")
        print("2) Iniciar sesión")
        print("3) Salir")
        op = pedir_opcion("Elegí una opción: ", {"1", "2", "3"})

        if op == "1":
            nombre = pedir_nombre()
            email = pedir_email()
            password = pedir_password()
            try:
                u = Usuario.registrar(nombre, email, password)
                print(f"✅ Registro OK. ¡Bienvenido/a {u.nombre}!")
            except Exception as e:
                print("❌ No se pudo registrar:", e)

        elif op == "2":
            email = pedir_email()
            password = getpass.getpass("Contraseña: ").strip()

            admin = Admin.login_admin(email, password)
            if admin:
                print(f"🎉 Login ADMIN OK. Hola {admin.nombre}!")
                menu_admin(admin)
                continue

            u = Usuario.inicio_sesion(email, password)
            if u:
                print(f"🎉 Login OK. Hola {u.nombre}!")
                menu_usuario(u)
            else:
                print("❌ Credenciales inválidas.")

        elif op == "3":
            print("Hasta luego 👋")
            break


if __name__ == "__main__":
    if "root@example.com" not in USERS_DB:
        try:
            Admin.registrar_admin("Root", "root@example.com", "admin123")
        except Exception:
            pass
    menu_auth()
