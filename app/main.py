from __future__ import annotations
from servicios.gestor_usuario import GestorUsuario
from modulos_main.menu_usuario import menu_usuario


def main():
    gestor_usuario = GestorUsuario()
    while True:
        print("\nSistema SmartHome - Ejecución en memoria")
        print("Usuario administrador por defecto: ggonzalez@gmail.com / gaston1234")
        print("1) Registrarse")
        print("2) Iniciar sesión")
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            try:
                dni = int(input("DNI: "))
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                email = input("Email: ")
                contrasena = input("Contraseña: ")

                gestor_usuario.registrar_usuario(dni, nombre, apellido, email, contrasena, rol="Usuario")

            except Exception as e:
                print(f"❌ Error al registrar usuario: {e}")

        elif op == "2":
            email = input("Email: ").strip()
            contrasena = input("Contraseña: ").strip()
            session = gestor_usuario.login(email, contrasena)
            if session:
                menu_usuario(session)
            else:
                print("❌ Credenciales inválidas.")

        elif op == "0":
            print("Gracias por utilizar nuestro sistema SmartHome. Hasta pronto.")
            break

        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    main()
