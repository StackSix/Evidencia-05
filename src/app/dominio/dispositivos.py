class Dispositivo:
    """Clase para manejar dispositivos del hogar inteligente."""

    def __init__(self, accion, id_dispositivo, id_habitacion, estado):
        self.accion = accion
        self.id_dispositivo = id_dispositivo
        self.id_habitacion = id_habitacion
        self.estado = estado

    @classmethod
    def crear_dispositivos(cls, accion, id_dispositivo, id_habitacion, estado):
        """Método de clase para crear un nuevo dispositivo."""
        return cls(accion, id_dispositivo, id_habitacion, estado)

    def borrar_dispositivos(self):
        """Elimina el dispositivo actual."""
        return True
    
    def ver_dispositivos(self):
        """Devuelve los datos del dispositivo."""
        return {
            "Accion": self.accion,
            "id_dispositivo": self.id_dispositivo,
            "lugar": self.id_habitacion,
            "estado": self.estado
        }

    def modificar_dispositivo(self, accion):
        """Ejecuta una acción sobre el dispositivo."""
        if accion == "apagar":
            self.estado = "apagado"
        elif accion == "encender":
            self.estado = "encendido"
        return True

    