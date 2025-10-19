from typing import List, Dict, Optional
from app.dao.automatizaciones_dao import AutomatizacionesDAO
from app.dominio.automatizacion import Automatizacion
from app.dao.dispositivos_dao import DispositivoDAO
from app.dao.domicilios_dao import DomiciliosDAO
from datetime import datetime, timedelta, time


def menu_crud_automatizacion():
    while True:
        print("CRUD - Automatizaciones")
        print(" 1) Ver Automatizaciones")
        print(" 2) Crear Automatización")
        print(" 3) Actualizar Automatización")
        print(" 4) Eliminar Automatización")
        print(" 0) Volver al menú anterior")
        print("Seleccione una opción: ")
        
        sop = input("> ")
        
        if sop == "1":
            ver_automatizaciones()
        elif sop == "2":
            registrar_automatizacion()
        elif sop == "3":
            actualizar_automatizacion()
        elif sop == "4":
            eliminar_automatizacion()
        elif sop == "0":
            break
        else:
            print("❌ Opción no válida. Intentelo de nuevo.")

def ver_automatizaciones():
    automatizaciones = AutomatizacionesDAO.obtener_todas_activas()
    if automatizaciones:
        for a in automatizaciones:
            print(f"{a.id_automatizacion} - {a.id_domicilio} - {a.nombre} - {a.accion} - ON: {a.hora_encendido} - OFF: {a.hora_apagado}")
    else:
        print("❌ No se encontraron automatizaciones activas.")

def registrar_automatizacion(session: Dict):
    print("\n📌 Registrar nueva automatización")

    # Pedir ID del domicilio
    id_hogar_input = input("Ingrese el ID del domicilio: ").strip()
    if not id_hogar_input.isdigit():
        print("❌ ID de domicilio inválido.")
        return
    id_hogar = int(id_hogar_input)

    # Pedir nombre de la automatización
    nombre = input("Ingrese un nombre para la automatización: ").strip()
    if not nombre:
        print("❌ El nombre no puede estar vacío.")
        return

    # Pedir acción que realizará
    accion = input("Ingrese la acción que realizará la automatización: ").strip()
    if not accion:
        print("❌ La acción no puede estar vacía.")
        return

    # Crear objeto automatización
    automatizacion = Automatizacion(
        id_automatizacion=None,
        id_hogar=id_hogar,
        nombre=nombre,
        accion=accion,
        estado=1,           # Activada por defecto
        hora_encendido=None,
        hora_apagado=None
    )

    try:
        # Registrar en la base
        nuevo_id = AutomatizacionesDAO.registrar_automatizacion(automatizacion)
        print(f"✅ Automatización registrada con ID {nuevo_id}.")

        # Preguntar si desea configurar horario ahora
        configurar = input("¿Desea configurar horario de encendido/apagado ahora? (s/n): ").lower()
        if configurar == "s":
            configurar_automatizacion_menu(session, nuevo_id)

    except Exception as e:
        print(f"❌ Error al registrar la automatización: {e}")

def actualizar_automatizacion(session: Dict):
    """
    Menú para actualizar una automatización existente.
    Pide al usuario ID de la automatización y los campos a modificar.
    """
    try:
        id_automatizacion = int(input("Ingrese ID de la automatización a actualizar: ").strip())
    except ValueError:
        print("❌ ID inválido.")
        return

    # Leer la automatización existente
    automatizacion = AutomatizacionesDAO.obtener_automatizacion(id_automatizacion)
    if not automatizacion:
        print("❌ Automatización no encontrada.")
        return

    # Validar permisos: dueño del domicilio o admin
    if (automatizacion.id_domicilio not in [d.id_domicilio for d in DomiciliosDAO.obtener_domicilio_usuario(session["dni"])]
        and session.get("rol") != "admin"):
        print("❌ No tienes permiso para actualizar esta automatización.")
        return

    # Pedir nuevos valores (dejar vacío para no modificar)
    nombre = input(f"Nuevo nombre ({automatizacion.nombre}): ").strip() or automatizacion.nombre
    accion = input(f"Nueva acción ({automatizacion.accion}): ").strip() or automatizacion.accion
    estado_input = input(f"Nuevo estado ({'activo' if automatizacion.estado else 'inactivo'}): ").strip()
    estado = automatizacion.estado
    if estado_input.lower() in ["activo", "1", "encendido"]:
        estado = 1
    elif estado_input.lower() in ["inactivo", "0", "apagado"]:
        estado = 0

    # Actualizar los campos en el objeto
    automatizacion.nombre = nombre
    automatizacion.accion = accion
    automatizacion.estado = estado

    # Guardar cambios en la base de datos
    try:
        if AutomatizacionesDAO.actualizar_automatizacion(automatizacion):
            print("✅ Automatización actualizada correctamente.")
        else:
            print("❌ No se pudo actualizar la automatización.")
    except Exception as e:
        print(f"❌ Error al actualizar la automatización: {e}")
        
    # Preguntar si quiere reconfigurar horarios
    opcion_horario = input("¿Desea reconfigurar los horarios de encendido/apagado? (s/n): ").strip().lower()
    if opcion_horario == "s":
        on = input(f"Ingrese hora de encendido ({automatizacion.hora_encendido or 'HH:MM'}): ").strip()
        off = input(f"Ingrese hora de apagado ({automatizacion.hora_apagado or 'HH:MM'}): ").strip()
        try:
            configurar_automatizacion_horaria(session, id_automatizacion, on, off)
            print("✅ Horario configurado correctamente.")
        except Exception as e:
            print(f"❌ Error al configurar horario: {e}")

def eliminar_automatizacion(session: Dict):
    """
    Menú para eliminar una automatización.
    Permite eliminar automatizaciones del usuario o, si es admin, de cualquier usuario.
    """
    try:
        id_automatizacion = int(input("Ingrese ID de la automatización a eliminar: ").strip())
    except ValueError:
        print("❌ ID inválido.")
        return

    # Leer la automatización
    automatizacion = AutomatizacionesDAO.obtener_automatizacion(id_automatizacion)
    if not automatizacion:
        print("❌ Automatización no encontrada.")
        return

    # Validar permisos: dueño del domicilio o admin
    domicilios_usuario = [d.id_domicilio for d in DomiciliosDAO.obtener_domicilio_usuario(session["dni"])]
    if automatizacion.id_domicilio not in domicilios_usuario and session.get("rol") != "admin":
        print("❌ No tienes permiso para eliminar esta automatización.")
        return

    # Confirmar eliminación
    confirmar = input(f"¿Está seguro que desea eliminar la automatización '{automatizacion.nombre}'? (s/n): ").strip().lower()
    if confirmar != "s":
        print("❌ Eliminación cancelada.")
        return

    try:
        if AutomatizacionesDAO.eliminar_automatizacion(id_automatizacion):
            print("✅ Automatización eliminada correctamente.")
        else:
            print("❌ No se pudo eliminar la automatización.")
    except Exception as e:
        print(f"❌ Error al eliminar la automatización: {e}")

def configurar_automatizacion_menu(session: Dict, id_automatizacion: int):
    "Función de menú para configurar horario de automatización. Pide al usuario las horas y llama a la función que actualiza la base."
    print("\n⏰ Configurar horario de la automatización")
    on = input("Ingrese hora de encendido (HH:MM): ").strip()
    off = input("Ingrese hora de apagado (HH:MM): ").strip()

    try:
        configurar_automatizacion_horaria(session, id_automatizacion, on, off)
        print("✅ Horario configurado correctamente.")
    except Exception as e:
        print(f"❌ Error al configurar horario: {e}")
        
def configurar_automatizacion_horaria(session: Dict, id_automatizacion: int, on: str, off: str) -> None:
    automatizacion = AutomatizacionesDAO.obtener_automatizacion(id_automatizacion)
    if not automatizacion:
        raise ValueError("Automatización no encontrada.")

    # Validar permisos
    if (automatizacion.id_domicilio not in [d.id_domicilio for d in DomiciliosDAO.obtener_domicilio_usuario(session["dni"])]
        and session.get("rol") != "admin"):
        raise PermissionError("No tiene permiso para modificar esta automatización.")

    automatizacion.configurar_horario(on, off)

    if not AutomatizacionesDAO.actualizar_automatizacion(automatizacion):
        raise ValueError("No se pudo actualizar la configuración horaria.")
        
def ejecutar_accion_automatica(automatizacion_id: int) -> str: #simplificar
        automatizacion = AutomatizacionesDAO.obtener_automatizacion(automatizacion_id)
        if not automatizacion:
            return "Automatización no existe."

        if not (automatizacion.hora_encendido and automatizacion.hora_apagado):
            return "No hay ninguna automatización configurada."

        # Convertir a datetime.time según tipo
        if isinstance(automatizacion.hora_encendido, timedelta):
            hora_encendido = timedelta_a_time(automatizacion.hora_encendido)
        elif isinstance(automatizacion.hora_encendido, str):
            hora_encendido = datetime.strptime(automatizacion.hora_encendido, "%H:%M").time()
        else:
            hora_encendido = automatizacion.hora_encendido

        if isinstance(automatizacion.hora_apagado, timedelta):
            hora_apagado = timedelta_a_time(automatizacion.hora_apagado)
        elif isinstance(automatizacion.hora_apagado, str):
            hora_apagado = datetime.strptime(automatizacion.hora_apagado, "%H:%M").time()
        else:
            hora_apagado = automatizacion.hora_apagado

        hora_actual = datetime.now().time()
        esta_en_horario = False

        # Control de horario, incluyendo cruces de medianoche
        if hora_encendido <= hora_apagado:
            if hora_encendido <= hora_actual < hora_apagado:
                esta_en_horario = True
        else:
            if hora_actual >= hora_encendido or hora_actual < hora_apagado:
                esta_en_horario = True

        # ⚡ Aplicar acción a todos los dispositivos del hogar
        dispositivos = DispositivoDAO.listar_por_hogar(automatizacion.id_hogar)
        if not dispositivos:
            return f"No hay dispositivos registrados para el hogar {automatizacion.id_hogar}."

        for dispositivo in dispositivos:
            if esta_en_horario:
                dispositivo.ejecutar_accion()
            else:
                dispositivo.detener_accion()

        return f"Acción automática ejecutada para {len(dispositivos)} dispositivo(s)."
    
def timedelta_a_time(td: timedelta) -> time:
        # Convierte un timedelta a datetime.time
        total_segundos = int(td.total_seconds())
        horas = total_segundos // 3600 % 24
        minutos = (total_segundos % 3600) // 60
        return time(hour=horas, minute=minutos)