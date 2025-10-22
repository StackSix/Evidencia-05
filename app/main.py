from __future__ import annotations
from servicios.gestor_domicilio import GestorDomicilio
from dao.domicilios_dao import DomiciliosDAO
from modulos_main.funciones_de_autenticacion import registrar_usuario, login
from modulos_main.menu_usuario import menu_usuario

def main():
    while True:
        print("\nSistema SmartHome - Ejecución en memoria")
        print("Usuario administrador por defecto: daniel@example.com / 12345678")
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

                registrar_usuario(dni, nombre, apellido, email, contrasena, rol="Usuario")

            except Exception as e:
                print(f"❌ Error al registrar usuario: {e}")

        elif op == "2":
            # Login
            email = input("Email: ").strip()
            contrasena = input("Contraseña: ").strip()
            session = login(email, contrasena)
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
