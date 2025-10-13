from typing import List, Dict, Optional
from app.dao.automatizaciones_dao import AutomatizacionesDAO
from app.dao.dispositivos_dao import DispositivoDAO
from app.dominio.automatizacion import Automatizacion
from datetime import datetime

class AutomatizacionService:
    @staticmethod
    def crear_automatizacion(current_user: Dict, id_hogar: int, nombre: str, accion: str, id_dispositivo_asociado: int) -> int:
        if not AutomatizacionesDAO.es_dueno_de_hogar(current_user.get("dni"), id_hogar) and current_user.get("rol") != "admin":
            raise PermissionError("No tienes permiso para crear automatizaciones en este hogar.")
        
        automatizacion = Automatizacion(
            id_automatizacion=None,
            id_hogar=id_hogar,
            nombre=nombre,
            accion=accion,
            id_dispositivo_asociado=id_dispositivo_asociado,
            estado=False,
            hora_encendido=None,
            hora_apagado=None
        )
        return AutomatizacionesDAO.crear(automatizacion)

    @staticmethod
    def eliminar_automatizacion(current_user: Dict, automatizacion_id: int) -> None:
        # Validar si el usuario es un administrador o el dueño de la automatización
        if not AutomatizacionesDAO.es_dueno_de_automatizacion(current_user.get("dni"), automatizacion_id) and current_user.get("rol") != "admin":
            raise PermissionError("No tienes permiso para eliminar esta automatización.")
        
        if not AutomatizacionesDAO.eliminar(automatizacion_id):
            raise ValueError(f"No se pudo eliminar la automatización con ID {automatizacion_id}. Puede que no exista.")

    @staticmethod
    def mostrar_detalles_automatizacion(current_user: Dict, automatizacion_id: int) -> Optional[Dict]:
        # Validar si el usuario es un administrador o el dueño de la automatización
        if not AutomatizacionesDAO.es_dueno_de_automatizacion(current_user.get("dni"), automatizacion_id) and current_user.get("rol") != "admin":
            raise PermissionError("No tienes permiso para ver los detalles de esta automatización.")
        
        automatizacion = AutomatizacionesDAO.leer(automatizacion_id)
        if automatizacion:
            return automatizacion.mostrar_detalles_automatizacion()
        return None

    @staticmethod
    def configurar_automatizacion_horaria(current_user: Dict, automatizacion_id: int, on: str, off: str) -> None:
        # Validar si el usuario es un administrador o el dueño de la automatización
        if not AutomatizacionesDAO.es_dueno_de_automatizacion(current_user.get("dni"), automatizacion_id) and current_user.get("rol") != "admin":
            raise PermissionError("No tienes permiso para configurar esta automatización.")
        
        automatizacion = AutomatizacionesDAO.leer(automatizacion_id)
        if not automatizacion:
            raise ValueError("Automatización no encontrada.")
            
        automatizacion.configurar_horario(on, off)
        if not AutomatizacionesDAO.actualizar(automatizacion):
            raise ValueError("No se pudo actualizar la configuración horaria.")

    @staticmethod
    def ejecutar_accion_automatica(automatizacion_id: int):
        automatizacion = AutomatizacionesDAO.leer(automatizacion_id)
        if not automatizacion or not automatizacion.estado:
            return "Automatización OFF o no existe."

        if not (automatizacion.hora_encendido and automatizacion.hora_apagado):
            return "No hay ninguna automatización configurada."
        
        hora_actual = datetime.now().strftime("%H:%M")
        esta_en_horario = False
        
        if automatizacion.hora_encendido <= automatizacion.hora_apagado:
            # Mismo día
            if automatizacion.hora_encendido <= hora_actual < automatizacion.hora_apagado:
                esta_en_horario = True
        else:
            # Cruza la noche
            if hora_actual >= automatizacion.hora_encendido or hora_actual < automatizacion.hora_apagado:
                esta_en_horario = True
        
        dispositivo_asociado = DispositivoDAO.leer(automatizacion.id_dispositivo_asociado)
        
        if esta_en_horario:
            dispositivo_asociado.ejecutar_accion()
        else:
            dispositivo_asociado.detener_accion()
            