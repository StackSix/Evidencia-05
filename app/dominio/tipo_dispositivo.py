class TipoDispositivo:
    """Clase para manejar tipos de dispositivos."""

    def __init__(self, id_tipo: int, tipo_dispositivo: str):
        self.__id_tipo = id_tipo
        self.__tipo_dispositivo = tipo_dispositivo
    
    @property
    def id_tipo(self) -> int:
        return self.__id_tipo
    
    @property
    def tipo_dispositivo(self) -> str:
        return self.__tipo_dispositivo
    
    def __str__(self):
        return f"TipoDispositivo(ID: {self.id_tipo}, Tipo: {self.tipo_dispositivo})"
        