class Domicilio:
    """Clase para manejar hogares."""

    def __init__(self,id_hogar, direccion, numeracion, ciudad, nombre_domicilio):
        self.id_hogar = id_hogar
        self.direccion = direccion
        self.numeracion = numeracion
        self.ciudad = ciudad
        self.nombre_domicilio = nombre_domicilio

    @classmethod
    def agregar_domicilio(cls, id_hogar, direccion, nombre, ):
        """Método de clase para agregar un nuevo hogar."""
        return cls(id_hogar, direccion, nombre, )

     #def eliminar_hogar(self):
        """Elimina el hogar actual."""
        # Falta completar!!!
        return True

    def ver_domicilios(self):
        """Devuelve los datos del hogar."""
        return {
            "id_hogar": self.id_hogar,
            "direccion": self.direccion,
            "numeracion": self.numeracion,
            "ciudad": self.ciudad,
            "domicilio": self.nombre_domicilio
        }