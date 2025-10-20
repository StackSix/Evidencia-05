from __future__ import annotations
from app.servicios.gestor_dispositivo import GestorDispositivo
from typing import Dict

def menu_crud_dispositivos(session: Dict, gestor: GestorDispositivo, nombre_domicilio: str):
    """
    Menú de interacción con dispositivos para un domicilio,
    separado del gestor. Recibe un GestorDispositivo.
    """
    while True:
        print("\nCRUD - Dispositivos")
        print(" 1) Ver dispositivos")
        print(" 2) Crear Dispositivo")
        print(" 3) Actualizar Dispositivo")
        print(" 4) Eliminar Dispositivo")
        print(" 0) Volver al menú anterior")
        opcion = input("> ").strip()

        if opcion == "1":
            gestor.listar_dispositivos(nombre_domicilio)

        elif opcion == "2":
            etiqueta = input("Ingrese una etiqueta para el dispositivo: ").strip()
            if not etiqueta:
                print("❌ La etiqueta no puede estar vacía.")
                continue

            id_tipo_input = input("Ingrese el ID del tipo de dispositivo: ").strip()
            if not id_tipo_input.isdigit():
                print("❌ ID de tipo inválido.")
                continue

            id_tipo = int(id_tipo_input)
            gestor.agregar_dispositivo(etiqueta, id_tipo)

        elif opcion == "3":
            id_disp_input = input("Ingrese el ID del dispositivo a actualizar: ").strip()
            if not id_disp_input.isdigit():
                print("❌ ID de dispositivo inválido.")
                continue
            id_dispositivo = int(id_disp_input)

            id_tipo_input = input("Ingrese el nuevo ID de tipo (deje vacío para no modificar): ").strip()
            id_tipo = int(id_tipo_input) if id_tipo_input else None

            etiqueta = input("Ingrese la nueva etiqueta (deje vacío para no modificar): ").strip() or None

            if id_tipo is None and etiqueta is None:
                print("⚠️ No se ingresó ningún cambio.")
                continue

            gestor.actualizar_dispositivo(id_dispositivo, id_tipo=id_tipo, etiqueta=etiqueta)

        elif opcion == "4":
            id_disp_input = input("Ingrese el ID del dispositivo a eliminar: ").strip()
            if not id_disp_input.isdigit():
                print("❌ ID inválido. Debe ser un número entero.")
                continue
            id_dispositivo = int(id_disp_input)

            confirm = input(f"¿Está seguro que desea eliminar el dispositivo con ID {id_dispositivo}? (s/n): ").lower()
            if confirm != "s":
                print("❎ Operación cancelada.")
                continue

            gestor.eliminar_dispositivo(id_dispositivo)

        elif opcion == "0":
            break

        else:
            print("❌ Opción no válida. Intentelo de nuevo.")
            