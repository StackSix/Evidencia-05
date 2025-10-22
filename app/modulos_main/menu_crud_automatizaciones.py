from __future__ import annotations
from typing import Dict
from servicios.gestor_automatizacion import GestorAutomatizacion
from dominio.automatizacion import Automatizacion
from modulos_main.funciones_de_automatizacion import pedir_hora


def menu_crud_automatizacion(session: Dict, gestor: GestorAutomatizacion):
    while True:
        print("\n CRUD - Automatizaciones")
        print(" 1) Ver Automatizaciones")
        print(" 2) Crear Automatización")
        print(" 3) Actualizar Automatización")
        print(" 4) Eliminar Automatización")
        print(" 0) Volver al menú anterior")
        
        opcion = input("> ").strip()

        if opcion == "1":
            gestor.listar(session.get("dni"))
        
        elif opcion == "2":
            id_domicilio = input("Ingrese ID del domicilio: ").strip()
            nombre = input("Ingrese nombre de la automatización: ").strip()
            accion = input("Ingrese acción de la automatización: ").strip()
            
            if not (id_domicilio.isdigit() and nombre and accion):
                print("❌ Datos inválidos, no se pudo crear la automatización.")
                continue
            
            # Pedir horarios al usuario
            hora_encendido = pedir_hora("Ingrese hora de encendido (HH:MM): ")
            hora_apagado = pedir_hora("Ingrese hora de apagado (HH:MM): ")

            
            automatizacion = Automatizacion(
                id_automatizacion=None,
                id_domicilio=int(id_domicilio),
                nombre=nombre,
                accion=accion,
                estado=False,
                hora_encendido=None,
                hora_apagado=None
            )
            
            # Configurar horario ingresado
            automatizacion.configurar_horario(hora_encendido, hora_apagado)
            # Registrar en el gestor/DAO
            gestor.registrar(automatizacion)  
            
        elif opcion == "3":
            id_auto = input("Ingrese ID de la automatización: ").strip()
            if not id_auto.isdigit():
                print("❌ ID inválido.")
                continue
            
            auto_existente = gestor.obtener_por_id(int(id_auto))
            if not auto_existente:
                print("❌ Automatización no encontrada.")
                continue
            
            nombre = input("Nuevo nombre (dejar vacío para no cambiar): ").strip()
            accion = input("Nueva acción (dejar vacío para no cambiar): ").strip()
            estado_input = input("Nuevo estado (activo/inactivo, dejar vacío para no cambiar): ").strip().lower()
            
            estado = None
            if estado_input in ["activo", "1", "encendido"]:
                estado = True
            elif estado_input in ["inactivo", "0", "apagado"]:
                estado = False
            
            # Preguntar si quiere cambiar los horarios
            cambiar_horarios = input("¿Desea actualizar los horarios? (s/n): ").strip().lower()
            if cambiar_horarios == "s":
                hora_encendido = pedir_hora("Ingrese nueva hora de encendido (HH:MM): ")
                hora_apagado = pedir_hora("Ingrese nueva hora de apagado (HH:MM): ")
                auto_existente.configurar_horario(hora_encendido, hora_apagado)
            # Actualizar en gestor y dao
            gestor.actualizar(auto_existente, nombre or None, accion or None, estado)
        
        elif opcion == "4":
            id_auto = input("Ingrese ID de la automatización a eliminar: ").strip()
            if not id_auto.isdigit():
                print("❌ ID inválido.")
                continue
            gestor.eliminar(int(id_auto))
        
        elif opcion == "0":
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")
            