from __future__ import annotations
from app.dao.automatizaciones_dao import AutomatizacionesDAO
from app.dominio.automatizacion import Automatizacion
from app.dao.dispositivos_dao import DispositivoDAO
from app.dao.domicilios_dao import DomiciliosDAO
from datetime import datetime, timedelta, time
        
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
        dispositivos = DispositivoDAO.listar_dispositivos_por_domicilio(automatizacion.id_hogar)
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
    