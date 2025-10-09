class Automatizacion:
    """Clase para manejar automatizaciones del hogar."""

    def __init__(self, id_automatizacion, id_hogar, nombre, accion):
        self.id_automatizacion = id_automatizacion
        self.id_hogar = id_hogar
        self.nombre = nombre
        self.accion = accion

    @classmethod
    def crear_automatizacion(cls, id_automatizacion, id_hogar, nombre, accion):
        """Método de clase para crear una nueva automatización."""
        return cls(id_automatizacion, id_hogar, nombre, accion)

    
    def eliminar_automatizaciones(self):
        """Elimina la automatización actual."""
        return True

    def mostrar_automatizaciones(self):
        """Devuelve los datos de la automatización."""
        return {
            "id_automatizacion": self.id_automatizacion,
            "id_hogar": self.id_hogar,
            "nombre": self.nombre,
            "accion": self.accion
        }
    #def monitor_automatizaciones_activas(self):
        """Monitorea las automatizaciones activas."""
        #hay que desarrollarla aun!!!!
        return True

    #def ejecutar_accion(self):
        """Ejecuta la acción de la automatización."""
        #hay que desarrollarla aun!!!!
        return True
