from __future__ import annotations

class Domicilio:
    "Clase para manejar hogares."
    def __init__(self, id_domicilio: int, direccion: str, ciudad: str, nombre_domicilio: str):
        self.id_domicilio = id_domicilio
        self.direccion = direccion
        self.ciudad = ciudad
        self.nombre_domicilio = nombre_domicilio

    def mostrar_datos_domicilio(self):
        "Devuelve los datos del hogar."
        return {
            "id_hogar": self.id_domicilio,
            "direccion": self.direccion,
            "ciudad": self.ciudad,
            "domicilio": self.nombre_domicilio
        }
        