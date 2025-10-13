from __future__ import annotations
from usuarios import Usuario


class Domicilio:
    "Clase para manejar hogares."

    def __init__(self, id_hogar, direccion, numeracion, ciudad, alias_domicilio):
        self.id_hogar = id_hogar
        self.direccion = direccion
        self.numeracion = numeracion
        self.ciudad = ciudad
        self.alias_domicilio = alias_domicilio

    def mostrar_datos_domicilio(self):
        "Devuelve los datos del hogar."
        return {
            "id_hogar": self.id_hogar,
            "direccion": self.direccion,
            "numeracion": self.numeracion,
            "ciudad": self.ciudad,
            "domicilio": self.alias_domicilio
        }
        