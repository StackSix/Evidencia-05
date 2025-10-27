from __future__ import annotations
from typing import Dict
from servicios.gestor_domicilio import GestorDomicilio
from servicios.gestor_usuario import GestorUsuario
from dao.domicilio_dao import DomicilioDAO


def menu_crud_domicilios(session: Dict, gestor_domicilio: GestorDomicilio):
    """
    Menú de interacción con domicilios, separado del gestor.
    Recibe un GestorDomicilio y llama sus métodos.
    """
    while True:
        print("\nCRUD - Domicilios")
        print(" 1) Ver domicilios de un usuario")
        print(" 2) Crear domicilio para un usuario")
        print(" 3) Actualizar domicilio")
        print(" 4) Eliminar domicilio")
        print(" 0) Volver al menú anterior")
        opcion = input("> ").strip()

        if opcion == "0":
            break

        gestor_usuario = GestorUsuario()
        usuarios = gestor_usuario.listar_usuarios()
        if not usuarios:
            print("❌ No hay usuarios registrados.")
            continue

        print("\n--- Seleccione un usuario ---")
        for u in usuarios:
            print(f"ID: {u.id_usuario} - {u.nombre} {u.apellido} ({u.rol})")

        try:
            id_usuario = int(input("Ingrese el ID del usuario: ").strip())
        except ValueError:
            print("❌ ID inválido.")
            continue

        domicilios_usuario = DomicilioDAO.obtener_domicilio_usuario(id_usuario)
        gestor_domicilio = GestorDomicilio(id_usuario=id_usuario, domicilios=domicilios_usuario)

        if opcion == "1":  
            gestor_domicilio.listar_domicilios()

        elif opcion == "2":  
            direccion = input("Ingrese la dirección: ").strip()
            ciudad = input("Ingrese la ciudad: ").strip()
            nombre_domicilio = input("Ingrese un nombre o alias para el domicilio: ").strip()
            if direccion and ciudad and nombre_domicilio:
                gestor_domicilio.agregar_domicilio(direccion, ciudad, nombre_domicilio)
            else:
                print("❌ Todos los campos son obligatorios.")

        elif opcion == "3": 
            gestor_domicilio.listar_domicilios()
            try:
                id_domicilio = int(input("Ingrese el ID del domicilio a actualizar: ").strip())
                direccion = input("Ingrese la nueva dirección: ").strip()
                ciudad = input("Ingrese la nueva ciudad: ").strip()
                nombre_domicilio = input("Ingrese el nuevo nombre o alias: ").strip()
                if direccion and ciudad and nombre_domicilio:
                    gestor_domicilio.actualizar_domicilio(id_domicilio, direccion, ciudad, nombre_domicilio)
                else:
                    print("❌ Todos los campos son obligatorios.")
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "4":  
            gestor_domicilio.listar_domicilios()
            try:
                id_domicilio = int(input("Ingrese el ID del domicilio a eliminar: ").strip())
                confirm = input(f"¿Está seguro de eliminar el domicilio con ID {id_domicilio}? (s/n): ").lower()
                if confirm == "s":
                    gestor_domicilio.eliminar_domicilio(id_domicilio)
                else:
                    print("❎ Operación cancelada.")
            except ValueError:
                print("❌ ID inválido.")

        else:
            print("❌ Opción no válida. Intente de nuevo.")
            