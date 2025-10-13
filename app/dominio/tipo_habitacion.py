
class Tipo_habitacion:
    "Clase para manejar ambientes de un hogar."
    def __init__(self, id_habitacion, id_hogar, nombre):
        self.id_habitacion = id_habitacion
        self.id_hogar = id_hogar
        self.nombre = nombre

    def mostrar_datos_habitacion(self):
        "Devuelve los datos del ambiente."
        return {
            "id_habitacion": self.id_habitacion,
            "id_hogar": self.id_hogar,
            "nombre": self.nombre
        }
        