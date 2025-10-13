from __future__ import annotations
from typing import Optional, Dict
from datetime import datetime
from app.dominio.dispositivos import Dispositivo


class Automatizacion:
    "Clase para manejar automatizaciones del hogar."
    def __init__(self, id_automatizacion: Optional[int], id_hogar: int, nombre: str, accion: str):
        self.id_automatizacion = id_automatizacion
        self.id_hogar = id_hogar
        self.nombre = nombre
        self.accion = accion

    def configurar_horario(self, on: str, off: str):
        "Configura las horas de encendido y apagado."
        self.hora_encendido = on
        self.hora_apagado = off
        self.estado = True
    
    def desactivar(self):
        "Desactiva la automatización."
        self.estado = False
        
    def mostrar_detalles_automatizacion(self) -> Dict:
        "Devuelve los datos de la automatización en formato de diccionario."
        return {
            "id_automatizacion": self.id_automatizacion,
            "id_hogar": self.id_hogar,
            "nombre": self.nombre,
            "accion": self.accion,
            "id_dispositivo_asociado": self.id_dispositivo_asociado,
            "estado": self.estado,
            "hora_encendido": self.hora_encendido,
            "hora_apagado": self.hora_apagado
        }
        