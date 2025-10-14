from typing import List, Dict, Optional
from app.dao.automatizaciones_dao import AutomatizacionesDAO
from app.dominio.automatizacion import Automatizacion
from app.dao.dispositivos_dao import DispositivoDAO
from datetime import datetime, timedelta, time


def timedelta_a_time(td: timedelta) -> time:
        # Convierte un timedelta a datetime.time
        total_segundos = int(td.total_seconds())
        horas = total_segundos // 3600 % 24
        minutos = (total_segundos % 3600) // 60
        return time(hour=horas, minute=minutos)

class AutomatizacionService:

    @staticmethod
    def crear_automatizacion(current_user: Dict, id_hogar: int, nombre: str, accion: str) -> int:
        """
        Crea una automatización asociada al usuario a través del hogar.
        """
        # Validar que el hogar pertenece al usuario o que es admin
        if not AutomatizacionesDAO.es_dueno_de_hogar(current_user.get("dni"), id_hogar) and current_user.get("rol") != "admin":
            raise PermissionError("No tienes permiso para crear automatizaciones en este hogar.")
        
        automatizacion = Automatizacion(
            id_automatizacion=None,
            id_hogar=id_hogar,
            nombre=nombre,
            accion=accion,
            hora_encendido=None,
            hora_apagado=None
        )

        # DAO crea la automatización en la base de datos
        return AutomatizacionesDAO.crear(automatizacion)

    @staticmethod
    def eliminar_automatizacion(current_user: Dict, automatizacion_id: int) -> None:
        """
        Elimina una automatización si pertenece al usuario o si es admin.
        """
        if not AutomatizacionesDAO.es_dueno_de_automatizacion(current_user.get("dni"), automatizacion_id) and current_user.get("rol") != "admin":
            raise PermissionError("No tienes permiso para eliminar esta automatización.")
        
        if not AutomatizacionesDAO.eliminar(automatizacion_id):
            raise ValueError(f"No se pudo eliminar la automatización con ID {automatizacion_id}.")

    @staticmethod
    def listar_automatizaciones_por_usuario(current_user: Dict) -> List[Dict]:
        """
        Devuelve todas las automatizaciones asociadas a los domicilios del usuario.
        """

        # Recupera los domicilios del usuario
        domicilios = AutomatizacionesDAO.listar_domicilios_del_usuario(current_user.get("dni"))
        domicilios_ids = [d['id_hogar'] for d in domicilios]

        # Recupera todas las automatizaciones y filtra por los domicilios del usuario
        todas = AutomatizacionesDAO.leer_todas()
        return [a for a in todas if a['id_hogar'] in domicilios_ids]
    
    @staticmethod
    def modificar_automatizacion(current_user: Dict, automatizacion_id: int, nuevo_nombre: Optional[str], nueva_accion: Optional[str]) -> None:
        """
        Modifica nombre y/o acción de una automatización si pertenece al usuario o es admin.
        """
        # Verificar propiedad o rol admin
        if not AutomatizacionesDAO.es_dueno_de_automatizacion(current_user.get("dni"), automatizacion_id) and current_user.get("rol") != "admin":
            raise PermissionError("No tienes permiso para modificar esta automatización.")

        # Leer automatización actual
        automatizacion = AutomatizacionesDAO.leer(automatizacion_id)
        if not automatizacion:
            raise ValueError(f"No se encontró la automatización con ID {automatizacion_id}.")

        # Actualizar solo los campos provistos
        if nuevo_nombre is not None:
            automatizacion.nombre = nuevo_nombre
        if nueva_accion is not None:
            automatizacion.accion = nueva_accion

        # Persistir cambios
        if not AutomatizacionesDAO.actualizar(automatizacion):
            raise RuntimeError(f"No se pudo actualizar la automatización con ID {automatizacion_id}.")
        
    @staticmethod
    def configurar_automatizacion_horaria(current_user: Dict, automatizacion_id: int, on: str, off: str) -> None:
        # Validar permisos
        if (not AutomatizacionesDAO.es_dueno_de_automatizacion(current_user.get("dni"), automatizacion_id)
                and current_user.get("rol") != "admin"):
            raise PermissionError("No tienes permiso de administrador para configurar esta automatización.")
        
        automatizacion = AutomatizacionesDAO.leer(automatizacion_id)
        if not automatizacion:
            raise ValueError("Automatización no encontrada.")
        
        # Configurar horario en el objeto
        automatizacion.configurar_horario(on, off)

        # Actualizar en la base
        if not AutomatizacionesDAO.actualizar(automatizacion):
            raise ValueError("No se pudo actualizar la configuración horaria.")
        
    

    @staticmethod
    def ejecutar_accion_automatica(automatizacion_id: int) -> str:
        automatizacion = AutomatizacionesDAO.leer(automatizacion_id)
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