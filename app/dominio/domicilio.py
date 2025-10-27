from __future__ import annotations
from typing import List
from servicios.gestor_dispositivo import GestorDispositivo

class Domicilio:
    "Clase para manejar hogares."
    def __init__(self, id_domicilio: int, direccion: str, ciudad: str, nombre_domicilio: str, gestor_dispositivos: GestorDispositivo = None):
        self.__id_domicilio = id_domicilio
        self.__direccion = direccion
        self.__ciudad = ciudad
        self.__nombre_domicilio = nombre_domicilio
        self.__gestor_dispositivos = gestor_dispositivos if gestor_dispositivos is not None else GestorDispositivo(id_domicilio)
        
    @property
    def id_domicilio(self) -> int:
        return self.__id_domicilio
    
    @id_domicilio.setter
    def id_domicilio(self, nuevo_id):
        if not isinstance(nuevo_id, int):
            raise TypeError("El id debe ser un número entero.")
        self.__id_domicilio = nuevo_id
    
    @property
    def direccion(self) -> str:
        return self.__direccion
    
    @direccion.setter
    def direccion(self, nueva_direccion):
        if not isinstance(nueva_direccion, str):
            raise TypeError("La dirección no es válida.")
        self.__direccion = nueva_direccion      
    
    @property
    def ciudad(self) -> str:
        return self.__ciudad
    
    @ciudad.setter
    def ciudad(self, nueva_ciudad):
        if not isinstance(nueva_ciudad, str):
            raise TypeError("La dirección no es válida.")
        self.__ciudad = nueva_ciudad 
    
    @property
    def nombre_domicilio(self) -> str:
        return self.__nombre_domicilio
    
    @nombre_domicilio.setter
    def nombre_domicilio(self, nuevo_nombre_domicilio):
        if not isinstance(nuevo_nombre_domicilio, str):
            raise TypeError("El nombre ingresado no es válido.")
        self.__nombre_domicilio = nuevo_nombre_domicilio
    
    @property    
    def gestor_dispositivos(self) -> GestorDispositivo:
        return self.__gestor_dispositivos
    
    def mostrar_datos_domicilio(self):
        return {
            "id_hogar": self.id_domicilio,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "domicilio": self.nombre_domicilio
        }
         