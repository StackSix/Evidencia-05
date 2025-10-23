from __future__ import annotations
from typing import Dict
from servicios.gestor_automatizacion import GestorAutomatizacion
from dominio.automatizacion import Automatizacion
from modulos_main.funciones_de_automatizacion import pedir_hora

def menu_crud_automatizacion(session: Dict, gestor: GestorAutomatizacion):
    """Menú CRUD para automatizaciones del usuario o administrador."""
    dni_usuario = session.get("dni")
    rol = session.get("rol", "usuario")

    while True:
        print("\n=== CRUD - Automatizaciones ===")
        print(" 1) Ver Automatizaciones")
        print(" 2) Crear Automatización")
        print(" 3) Actualizar Automatización")
        print(" 4) Eliminar Automatización")
        print(" 0) Volver al menú anterior")
        opcion = input("> ").strip()

        if opcion == "1":
            if rol == "admin":
                gestor.listar()  
            else:
                gestor.listar(dni_usuario)

        elif opcion == "2":
            print("\n📍 Creación de nueva automatización")
            id_domicilio = input("Ingrese ID del domicilio: ").strip()
            nombre = input("Ingrese nombre de la automatización: ").strip()
            accion = input("Ingrese acción (ej: encender luces, abrir portón): ").strip()
            hora_on = pedir_hora("Ingrese hora de encendido (HH:MM): ")
            hora_off = pedir_hora("Ingrese hora de apagado (HH:MM): ")
            
            automatizacion = Automatizacion(
                id_automatizacion=None,
                id_domicilio=id_domicilio,
                nombre=nombre,
                accion=accion,
                estado=False,
                hora_encendido=hora_on,
                hora_apagado=hora_off
            )

            gestor.registrar(automatizacion)
            print("✅ Automatización creada con éxito.")

        elif opcion == "3":
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

            estado = None
            if estado_input in ["activo", "1", "encendido"]:
                estado = True
            elif estado_input in ["inactivo", "0", "apagado"]:
                estado = False

            if input("¿Actualizar horarios? (s/n): ").strip().lower() == "s":
                hora_on = pedir_hora("Nueva hora de encendido (HH:MM): ")
                hora_off = pedir_hora("Nueva hora de apagado (HH:MM): ")
                existente.configurar_horario(hora_on, hora_off)

            gestor.actualizar(existente, nombre or None, accion or None, estado)

        elif opcion == "4":
            id_automatizacion = input("Ingrese ID de la automatización a eliminar: ").strip()
            if not id_automatizacion.isdigit():
                print("❌ ID inválido.")
                continue
            gestor.eliminar(int(id_automatizacion))

        elif opcion == "0":
            print("↩️ Volviendo al menú anterior...")
            break

        else:
            print("❌ Opción no válida.")