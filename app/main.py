from app.servicios.auth_service import AuthService
from app.servicios.usuarios_service import UsuariosService
from app.servicios.dispositivos_service import DispositivosService
from app.servicios.domicilios_service import DomiciliosService
from app.servicios.habitacion_service import HabitacionService

def menu_usuario(session):
    print(f"\nBienvenido/a {session['nombre']} ({session['rol']})")
    while True:
        print("\n1) Ver mis domicilios")
        print("2) Ver mis dispositivos")
        if session["rol"] == "admin":
            print("3) [ADMIN] Crear dispositivo")
            print("4) [ADMIN] Cambiar rol de usuario")
        print("0) Salir")
        op = input("> ")
        if op == "1":
            hogares = DomiciliosService.listar_por_usuario(session["id"])
            for h in hogares:
                print(h)
        elif op == "2":
            devs = DispositivosService.listar_por_usuario(session["id"])
            for d in devs:
                print(d)
        elif op == "3" and session["rol"] == "admin":
            id_hab = input("id_habitacion (vacío=Null): ").strip() or None
            id_tipo = int(input("id_tipo: "))
            etiqueta = input("etiqueta: ")
            nuevo_id = DispositivosService.crear_admin(session, int(id_hab) if id_hab else None, id_tipo, etiqueta)
            print("creado id:", nuevo_id)
        elif op == "4" and session["rol"] == "admin":
            uid = int(input("user_id a cambiar: "))
            nr = input("nuevo rol [admin/usuario]: ")
            UsuariosService.cambiar_rol_admin(session, uid, nr)
            print("ok")
        elif op == "0":
            break

def main():
    print("1) Registrarse")
    print("2) Iniciar sesión")
    print("3) Recuperar contraseña")
    op = input("> ")
    if op == "1":
        dni = int(input("DNI: "))
        id_rol = 2  # usuario por defecto
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        email = input("Email: ")
        pw = input("Contraseña: ")
        uid = AuthService.registrar_usuario(dni, id_rol, nombre, apellido, email, pw, "usuario")
        print("Usuario creado con id:", uid)
    elif op == "2":
        email = input("Email: ")
        pw = input("Contraseña: ")
        session = AuthService.login(email, pw)
        if not session:
            print("Credenciales inválidas.")
            return
        menu_usuario(session)
    elif op == "3":
        email = input("Email: ")
        dni = int(input("DNI: "))
        nueva = input("Nueva contraseña: ")
        ok = AuthService.resetear_contrasena(email, dni, nueva)
        print("Listo" if ok else "No se pudo resetear (email/dni incorrectos).")

if __name__ == "__main__":
    main()
