from __future__ import annotations
from typing import Dict
from app.servicios.gestor_automatizacion import GestorAutomatizacion
from app.dominio.automatizacion import Automatizacion


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
            id_hogar = input("Ingrese ID del domicilio: ").strip()
            nombre = input("Ingrese nombre de la automatización: ").strip()
            accion = input("Ingrese acción de la automatización: ").strip()
            
            if not (id_hogar.isdigit() and nombre and accion):
                print("❌ Datos inválidos, no se pudo crear la automatización.")
                continue
            
            automatizacion = Automatizacion(
                id_automatizacion=None,
                id_hogar=int(id_hogar),
                nombre=nombre,
                accion=accion,
                estado=1,
                hora_encendido=None,
                hora_apagado=None
            )
            gestor.registrar(automatizacion)  # Llama al gestor que hace todo
            
        elif opcion == "3":
            id_auto = input("Ingrese ID de la automatización: ").strip()
            if not id_auto.isdigit():
                print("❌ ID inválido.")
                continue
            
            nombre = input("Nuevo nombre (dejar vacío para no cambiar): ").strip()
            accion = input("Nueva acción (dejar vacío para no cambiar): ").strip()
            estado_input = input("Nuevo estado (activo/inactivo, dejar vacío para no cambiar): ").strip().lower()
            
            estado = None
            if estado_input in ["activo", "1", "encendido"]:
                estado = 1
            elif estado_input in ["inactivo", "0", "apagado"]:
                estado = 0
            
            auto_existente = gestor.obtener_por_id(int(id_auto))
            if not auto_existente:
                print("❌ Automatización no encontrada.")
                continue
            
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
            