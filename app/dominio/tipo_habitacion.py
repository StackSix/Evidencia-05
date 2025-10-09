class Tipo_habitacion:
    """Clase para manejar ambientes de un hogar."""

    def __init__(self, id_habitacion, id_hogar, nombre):
        self.id_habitacion = id_habitacion
        self.id_hogar = id_hogar
        self.nombre = nombre

    @classmethod
    
    def gestionar_habitaciones(self, accion, datos=None):
        """Gestiona operaciones sobre el ambiente."""
        if accion == "actualizar" and datos:
            if "nombre" in datos:
                self.nombre = datos["nombre"]
        return True
    def crear_habitacion(cls, id_habitacion, id_hogar, nombre):
        """Método de clase para crear un nuevo ambiente."""
        return cls(id_habitacion, id_hogar, nombre)

    

    def ver_habitaciones(self):
        """Devuelve los datos del ambiente."""
        return {
            "id_ambiente": self.id_ambiente,
            "id_hogar": self.id_hogar,
            "nombre": self.nombre
        }

    def eliminar_habitaciones(self):
        """Elimina el ambiente actual."""
        return True