from __future__ import annotations

# Imports estándar que faltaban
import logging
from datetime import datetime
from enum import Enum

# Imports tolerantes (paquete o relativo)
try:
    # cuando ejecutás: PYTHONPATH=src python -m smarthome.router
    from smarthome.dispositivos import Dispositivo
    from smarthome.control_automatizacion import ControlAutomatizacion
    from smarthome.evento_dispositivo import EventoDispositivo
except ImportError:
    # cuando ejecutás: python camara.py / python router.py dentro de src/smarthome
    from .dispositivos import Dispositivo
    from .control_automatizacion import ControlAutomatizacion
    from .evento_dispositivo import EventoDispositivo

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class ModoGrabacion(Enum):
    MANUAL = "Manual"
    AUTOMATICO = "Automático"


class Camara(Dispositivo, ControlAutomatizacion):
    """
    Entidad Camara: graba en modo manual o automático y soporta automatización horaria.
    """
    def __init__(
        self,
        tipo: str,
        estado_dispositivo: str,
        nombre: str,
        modelo: str,
        grabacion_modo: ModoGrabacion = ModoGrabacion.MANUAL,
        modo_grabando: bool = False,
        estado_automatizacion: bool = False
    ) -> None:
        super().__init__(tipo, estado_dispositivo)
        self.__nombre = nombre
        self.__modelo = modelo
        self.__grabacion_modo = grabacion_modo
        self.__modo_grabando = modo_grabando
        self.__estado_automatizacion = estado_automatizacion
        self.__hora_encendido: str | None = None
        self.__hora_apagado: str | None = None
        self.__ultima_notificacion: bool | None = None

    # -------- Propiedades --------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str) -> None:
        if not nuevo_nombre:
            raise ValueError("El nombre de la cámara no puede estar vacío.")
        self.__nombre = nuevo_nombre

    @property
    def modelo(self) -> str:
        return self.__modelo

    @modelo.setter
    def modelo(self, nuevo_modelo: str) -> None:
        if not nuevo_modelo:
            raise ValueError("El modelo ingresado no puede estar vacío.")
        self.__modelo = nuevo_modelo

    @property
    def grabacion_modo(self) -> ModoGrabacion:
        return self.__grabacion_modo

    @grabacion_modo.setter
    def grabacion_modo(self, modo: ModoGrabacion) -> None:
        if not isinstance(modo, ModoGrabacion):
            raise ValueError("El modo de grabación es inválido.")
        self.__grabacion_modo = modo

    @property
    def modo_grabando(self) -> bool:
        return self.__modo_grabando

    @property
    def estado_automatizacion(self) -> bool:
        return self.__estado_automatizacion

    @estado_automatizacion.setter
    def estado_automatizacion(self, estado_automatizacion: bool) -> None:
        if not isinstance(estado_automatizacion, bool):
            raise ValueError("El estado ingresado no es válido.")
        self.__estado_automatizacion = estado_automatizacion
        
    @property
    def hora_encendido(self) -> str | None:
        return self.__hora_encendido
    
    @hora_encendido.setter
    def hora_encendido(self, on):
        if not isinstance(on, str):
            raise TypeError("El horario ingresado no es válido.")
        self.__hora_encendido = on
    
    @property
    def hora_apagado(self) -> str | None:
        return self.__hora_apagado
    
    @hora_apagado.setter
    def hora_apagado(self, off):
        if not isinstance(off, str):
            raise TypeError("El horario ingresado no es válido.")
        self.__hora_apagado = off
        
    @property
    def ultima_notificacion(self) -> bool | None:
        return self.__ultima_notificacion
    
    @ultima_notificacion.setter
    def ultima_notificacion(self, ultima_notificacion):
        if not isinstance(ultima_notificacion, bool):
            raise TypeError("El valor ingresado no es válido.")

    def __str__(self) -> str:
        return (
            super().__str__()
            + f"Nombre: {self.nombre} \n"
              f"Modelo: {self.modelo} \n"
              f"Grabacion Modo: {self.grabacion_modo} \n"
              f"Automatización: {self.estado_automatizacion} \n"
        )

    # -------- Comportamiento --------
    def grabar_manual(self, rec: bool) -> str:
        if self.grabacion_modo != ModoGrabacion.MANUAL:
            logger.warning("Intento de grabación Manual en modo Automático")
            return "El modo grabación es AUTOMÁTICO. Cámbielo a MANUAL e inténtelo nuevamente."

        if not isinstance(rec, bool):
            raise ValueError("Error. Debe ingresar una opción válida.")

        self.__modo_grabando = rec
        estado = "Grabando." if rec else "Guardando."
        logger.info(f"{self.nombre}: {estado}")
        return estado

    def modificar_grabacion_modo(self, automatico: bool) -> str:
        self.__grabacion_modo = ModoGrabacion.AUTOMATICO if automatico else ModoGrabacion.MANUAL
        if not automatico:
            self.__modo_grabando = False
        mensaje = f"Modo {self.__grabacion_modo.value} activado."
        logger.info(f"{self.nombre}: {mensaje}")
        return mensaje

    def grabar_automatico(self) -> str:
        if not self.estado_automatizacion:
            self.__modo_grabando = False
            logger.warning("Automatización apagada.")
            return "Automatización apagada"

        if self.hora_encendido and self.hora_apagado:
            hora_actual = datetime.now().strftime("%H:%M")

            if self.hora_encendido <= self.hora_apagado:
                # mismo día
                if self.hora_encendido <= hora_actual < self.hora_apagado:
                    self.__modo_grabando = True
                    return f"{self.nombre} está grabando"
            else:
                # cruza la noche
                if hora_actual >= self.hora_encendido or hora_actual < self.hora_apagado:
                    self.__modo_grabando = True
                    return f"{self.nombre} está grabando"

        self.__modo_grabando = False
        return f"{self.nombre} no está grabando"

    def procesar_notificacion(self) -> None:
        if not (self.hora_encendido and self.hora_apagado):
            logger.info("No hay horarios configurados.")
            return

        hora_actual = datetime.now().strftime("%H:%M")
        notificacion = EventoDispositivo()
        if hora_actual == self.hora_encendido:
            mensaje = notificacion.enviar_notificacion(True)
            self.ultima_notificacion = True
            logger.info(f"{self.nombre}: Notificación de inicio enviada.")
            return mensaje
        
        elif hora_actual == self.hora_apagado:
            mensaje = notificacion.enviar_notificacion(False)     
            self.ultima_notificacion = False
            logger.info(f"{self.nombre}: Notificación de apagado enviada")
            return mensaje
    

    # -------- Interfaz de automatización --------
    def configurar_automatizacion_horaria(self, on: str, off: str) -> str:
        if self.estado_dispositivo != "encendido":
            return "La camara debe estar encendida."

        self.estado_automatizacion = True
        self.hora_encendido = on
        self.hora_apagado = off
        self.__grabacion_modo = ModoGrabacion.AUTOMATICO
        return f"Automatización configurada: ON: {self.hora_encendido} OFF: {self.hora_apagado}"

    def mostrar_automatizacion(self) -> str:
        if not self.estado_automatizacion:
            logger.info(f"{self.nombre}: Automatización no configurada.")
            return "Automatización no configurada."

        return (
            "Automatización configurada.\n"
            f"Hora de Inicio: {self.hora_encendido}\n"
            f"Hora de Finalización {self.hora_apagado}\n"
        )
    