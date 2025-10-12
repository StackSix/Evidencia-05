from __future__ import annotations
from typing import Optional
from datetime import datetime

class Automatizacion:
    "Clase para manejar automatizaciones del hogar."

    def __init__(self, id_automatizacion: Optional[int], id_hogar: int, nombre: str, accion: str, dispositivo_asociado: any, estado: bool):
        self.id_automatizacion = id_automatizacion
        self.id_hogar = id_hogar
        self.nombre = nombre
        self.accion = accion
        self.dispositivo_asociado = dispositivo_asociado
        self.estado = estado
        self.hora_encendido: str | None = None
        self.hora_apagado: str | None = None

    @classmethod
    def crear_automatizacion(cls, id_hogar: int, nombre: str, accion: str, dispositivo_asociado: any):
        "Método de clase para crear una nueva automatización."
        return cls(None, id_hogar, nombre, accion, dispositivo_asociado, False)

    
    def eliminar_automatizaciones(self):
        "Elimina la automatización actual."
        return True

    def mostrar_automatizaciones(self):
        "Devuelve los datos de la automatización."
        return {
            "id_automatizacion": self.id_automatizacion,
            "id_hogar": self.id_hogar,
            "nombre": self.nombre,
            "accion": self.accion
        }
    
    def configurar_automatizacion_horaria(self, on: str, off: str) -> str:
        "Configura una automatización horaria."
        self.estado = True
        self.hora_encendido = on
        self.hora_apagado = off
        return f"Automatización configurada: ON: {self.hora_encendido} OFF: {self.hora_apagado}"
    
    def mostrar_automatizacion(self) -> str:
        if not self.estado:
            return "Automatización no configurada."
        return (
            "Automatización configurada.\n"
            f"Hora de Inicio: {self.hora_encendido}\n"
            f"Hora de Finalización {self.hora_apagado}\n"
        )
    
    def ejecutar_accion_automatica(self):
        "Ejecuta la acción con programación horaria."
        if not self.estado:
            return "Automatización OFF"

        if not (self.hora_encendido and self.hora_apagado):
            return "No hay ninguna automatización configurada."
        
        hora_actual = datetime.now().strftime("%H:%M")
        esta_en_horario = False
        
        if self.hora_encendido <= self.hora_apagado:
            # mismo día
            if self.hora_encendido <= hora_actual < self.hora_apagado:
                esta_en_horario = True
        else:
            # cruza la noche
            if hora_actual >= self.hora_encendido or hora_actual < self.hora_apagado:
                esta_en_horario = True
        
        if esta_en_horario:
            return self.dispositivo_asociado.ejecutar_accion(self.accion)
        else:
            return self.dispositivo_asociado.detener_accion(self.accion)