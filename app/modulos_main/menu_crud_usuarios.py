from app.servicios.gestor_usuario import GestorUsuario

def menu_crud_usuarios(gestor: GestorUsuario):
    """Menú de interacción con usuarios, separado del gestor."""
    while True:
        print("\nCRUD - Usuarios")
        print(" 1) Ver Usuarios Registrados")
        print(" 2) Actualizar Usuario")
        print(" 3) Eliminar Usuario")
        print(" 4) Modificar Rol de Usuario")
        print(" 0) Volver al menú anterior")
        opcion = input("> ").strip()

        if opcion == "1":
            gestor.listar_usuarios()

        elif opcion == "2":
            email = input("Ingrese el email del usuario a actualizar: ").strip()
            nombre = input("Nuevo nombre: ").strip()
            apellido = input("Nuevo apellido: ").strip()
            contrasena = input("Nueva contraseña: ").strip()
            gestor.actualizar_usuario(email, nombre, apellido, contrasena)

        elif opcion == "3":
            try:
                id_usuario = int(input("Ingrese el ID del usuario a eliminar: ").strip())
                confirm = input(f"¿Está seguro de eliminar el usuario con ID {id_usuario}? (s/n): ").lower()
                if confirm == "s":
                    gestor.eliminar_usuario(id_usuario)
                else:
                    print("❎ Operación cancelada.")
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "4":
            try:
                id_usuario = int(input("Ingrese el ID del usuario: ").strip())
                nuevo_id_rol = int(input("Ingrese el nuevo ID de rol: ").strip())
                gestor.modificar_rol(id_usuario, nuevo_id_rol)
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "0":
            break
        else:
            print("❌ Opción no válida.")