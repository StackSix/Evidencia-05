from __future__ import annotations
from app.servicios.gestor_domicilio import GestorDomicilio
from app.dao.domicilios_dao import DomiciliosDAO
from app.modulos_main.funciones_de_autenticacion import registrar_usuario, login
from app.modulos_main.menu_usuario import menu_usuario

def main():
    while True:
        print("\nSistema SmartHome - Ejecución en memoria")
        print("Usuario administrador por defecto: daniel@example.com / 12345678")
        print("1) Registrarse")
        print("2) Iniciar sesión")
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            # Registrar usuario
            try:
                dni = int(input("DNI: "))
                id_rol = 2  # usuario por defecto
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                email = input("Email: ")
                contrasena = input("Contraseña: ")

                registrar_usuario(dni, id_rol, nombre, apellido, email, contrasena)
                
                # Registrar domicilio inicial
                print("\n🏠 Registrar tu domicilio principal")
                id_domicilio = GestorDomicilio.agregar_domicilio()
                if id_domicilio:
                    DomiciliosDAO.vincular_usuario(dni, id_domicilio)
                    print(f"✅ Domicilio vinculado al usuario (ID domicilio: {id_domicilio})")

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
