from __future__ import annotations
from typing import Optional, Dict
from datetime import datetime
from app.dominio.dispositivos import Dispositivo


class Automatizacion:
    "Clase para manejar automatizaciones del hogar."
    def __init__(self, id_automatizacion: Optional[int], id_domicilio: int, nombre: str, accion: str, hora_encendido:str | None = None, hora_apagado:str | None = None):
        self.__id_automatizacion = id_automatizacion
        self.__id_domicilio = id_domicilio
        self.__nombre = nombre
        self.__accion = accion
        self.__hora_encendido = hora_encendido
        self.__hora_apagado = hora_apagado
        
    @property
    def id_automatizacion(self) -> int:
        return self.__id_automatizacion
    
    @property
    def id_domicilio(self) -> int:
        return self.__id_domicilio
    
    @id_domicilio.setter
    def id_domicilio(self, nuevo_id_domicilio):
        if not isinstance(nuevo_id_domicilio, int):
            raise TypeError("Debe ingresar un numero entero.")
        self.__id_domicilio = nuevo_id_domicilio
        
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        if not isinstance(nuevo_nombre, int):
            raise TypeError("Debe ingresar un numero entero.")
        self.__nombre = nuevo_nombre
    
    @property
    def accion(self) -> str:
        return self.__accion
    
    @accion.setter
    def accion(self, nueva_accion):
        if not isinstance(nueva_accion, int):
            raise TypeError("Debe ingresar un numero entero.")
        self.__accion = nueva_accion
    
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
            "id_automatizacion": self.__id_automatizacion,
            "id_hogar": self.__id_domicilio,
            "nombre": self.__nombre,
            "accion": self.__accion,
            "estado": self.estado,
            "hora_encendido": self.__hora_encendido,
            "hora_apagado": self.__hora_apagado
        }
        