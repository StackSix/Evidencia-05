from __future__ import annotations
from typing import Dict
from app.servicios.gestor_automatizacion import GestorAutomatizacion
from app.dominio.automatizacion import Automatizacion
from app.dao.domicilio_dao import DomicilioDAO


def menu_crud_automatizacion(session: Dict, gestor: GestorAutomatizacion):
    """Menú CRUD de automatizaciones (asume admin)."""
    while True:
        print("\n=== CRUD - Automatizaciones (Admin) ===")
        print(" 1) Ver Todas las Automatizaciones")
        print(" 2) Crear Automatización")
        print(" 3) Actualizar Automatización")
        print(" 4) Eliminar Automatización")
        print(" 0) Volver al menú anterior")
        opcion = input("> ").strip()

        if opcion == "1":
            gestor.listar()

        elif opcion == "2":
            print("\n⏰ Creación de nueva automatización ⚙️")
            print("\n--- Domicilios disponibles ---")
            for d in DomicilioDAO.obtener_todos_domicilios():
                print(f"- ID: {d.id_domicilio} | {d.nombre_domicilio} | {d.direccion} ({d.ciudad})")
            id_domicilio = input("Ingrese ID del domicilio: ").strip()
            nombre = input("Ingrese nombre de la automatización: ").strip()
            accion = input("Ingrese acción (ej: encender luces, abrir portón): ").strip()
            
            usar_horario_por_defecto = input("¿Usar horario por defecto (08:00-22:00)? [s/n]: ").lower() == "s"
    
            if usar_horario_por_defecto:
                hora_encendido, hora_apagado = None, None
            else:
                hora_encendido = gestor.pedir_hora("Ingrese hora de encendido (HH:MM): ")
                hora_apagado = gestor.pedir_hora("Ingrese hora de apagado (HH:MM): ")

            # Crear el objeto Automatizacion
            automatizacion = Automatizacion(
                id_automatizacion=None,
                id_domicilio=int(id_domicilio),
                nombre=nombre,
                accion=accion,
                estado=False,
                hora_encendido=hora_encendido,
                hora_apagado=hora_apagado
            )

            # Registrar en el gestor
            gestor.registrar(automatizacion)

        elif opcion == "3":
            gestor.listar()
            id_auto = input("Ingrese ID de la automatización: ").strip()
            if not id_auto.isdigit():
                print("❌ ID inválido.")
                continue

            existente = gestor.obtener_por_id(int(id_auto))
            if not existente:
                print("❌ Automatización no encontrada.")
                continue

            nombre = input("Nuevo nombre (enter para mantener): ").strip()
            accion = input("Nueva acción (enter para mantener): ").strip()
            estado_input = input("Nuevo estado (activo/inactivo, enter para mantener): ").strip().lower()

            if nombre:
                existente.nombre = nombre
            if accion:
                existente.accion = accion
            
            if estado_input in ["activo"]:
                existente.estado = True
            elif estado_input in ["inactivo"]:
                existente.estado = False

            if input("¿Actualizar horarios? (s/n): ").strip().lower() == "s":
                hora_encendido = gestor.pedir_hora("Nueva hora de encendido (HH:MM): ")
                hora_apagado = gestor.pedir_hora("Nueva hora de apagado (HH:MM): ")
                existente.configurar_horario(hora_encendido, hora_apagado)

            # Actualizar automatización
            gestor.actualizar(existente)

        elif opcion == "4":
            id_auto = input("Ingrese ID de la automatización a eliminar: ").strip()
            if not id_auto.isdigit():
                print("❌ ID inválido.")
                continue
            gestor.eliminar(int(id_auto))

        elif opcion == "0":
            print("↩️ Volviendo al menú anterior...")
            break
        else:
            print("❌ Opción no válida.")
            