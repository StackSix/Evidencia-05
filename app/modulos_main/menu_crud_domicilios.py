from __future__ import annotations
from servicios.gestor_domicilio import GestorDomicilio
from typing import Dict

def menu_crud_domicilios(session: Dict, gestor: GestorDomicilio):
    """
    Menú de interacción con domicilios, separado del gestor.
    Recibe un GestorDomicilio y llama sus métodos.
    """
    while True:
        print("\nCRUD - Domicilios")
        print(" 1) Ver domicilios")
        print(" 2) Crear domicilio")
        print(" 3) Actualizar domicilio")
        print(" 4) Eliminar domicilio")
        print(" 0) Volver al menú anterior")
        opcion = input("> ").strip()

        if opcion == "1":
            gestor.listar_domicilios()

        elif opcion == "2":
            direccion = input("Ingrese la dirección: ").strip()
            numeracion = input("Ingrese la numeración: ").strip()
            ciudad = input("Ingrese la ciudad: ").strip()
            nombre_domicilio = input("Ingrese un nombre o alias para el domicilio: ").strip()
            id_usuario = session.get("id_usuario")
            
            if direccion and numeracion and ciudad and nombre_domicilio:
                gestor.agregar_domicilio(direccion, numeracion, ciudad, nombre_domicilio, id_usuario)
            else:
                print("❌ Todos los campos son obligatorios.")

        elif opcion == "3":
            try:
                id_domicilio = int(input("Ingrese el ID del domicilio a actualizar: ").strip())
                direccion = input("Ingrese la nueva dirección: ").strip()
                numeracion = input("Ingrese la nueva numeración: ").strip()
                ciudad = input("Ingrese la nueva ciudad: ").strip()
                nombre_domicilio = input("Ingrese el nuevo nombre o alias del domicilio: ").strip()

                if direccion and numeracion and ciudad and nombre_domicilio:
                    gestor.actualizar_domicilio(id_domicilio, direccion, numeracion, ciudad, nombre_domicilio)
                else:
                    print("❌ Todos los campos son obligatorios.")
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "4":
            try:
                id_domicilio = int(input("Ingrese el ID del domicilio a eliminar: ").strip())
                confirm = input(f"¿Está seguro de eliminar el domicilio con ID {id_domicilio}? (s/n): ").lower()
                if confirm == "s":
                    gestor.eliminar_domicilio(id_domicilio)
                else:
                    print("❎ Operación cancelada.")
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "0":
            break

        else:
            print("❌ Opción no válida.")
            