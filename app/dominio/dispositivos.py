
class Dispositivo:
    "Clase para manejar dispositivos del hogar inteligente."

    def __init__(self, id_dispositivo: int, id_domicilio: int, id_tipo: int, estado: str, etiqueta: str):
        self.__id_dispositivo = id_dispositivo
        self.__id_domicilio = id_domicilio
        self.__id_tipo = id_tipo
        self.__estado = estado
        self.__etiqueta = etiqueta

    @property
    def id_dispositivo(self) -> int:
        return self.__id_dispositivo
        
    @property
    def id_domicilio(self) -> int:
        return self.__id_domicilio
    
    @id_domicilio.setter
    def id_domicilio(self, nuevo_id_domicilio):
        if not isinstance(nuevo_id_domicilio, int):
            raise TypeError("El id debe ser un número entero.")
        self.__id_domicilio = nuevo_id_domicilio
        
    @property
    def id_tipo(self) -> int:
        return self.__id_tipo
    
    @id_tipo.setter
    def id_tipo(self, nuevo_id_tipo):
        if not isinstance(nuevo_id_tipo, int):
            raise TypeError("El id debe ser un número entero.")
        self.__id_tipo = nuevo_id_tipo
    
    @property
    def estado(self) -> str:
        return self.__estado
    
    @estado.setter
    def estado(self, nuevo_estado):
        if nuevo_estado not in ["encendido", "apagado"]:
            raise ValueError("El estado no es válido. Debe ser 'encendido' o 'apagado'.")
        self.__estado = nuevo_estado
        
    @property
    def etiqueta(self) -> str:
        return self.__etiqueta
    
    @etiqueta.setter
    def etiqueta(self, nueva_etiqueta):
        if not isinstance(nueva_etiqueta, str):
            raise TypeError("La etiqueta no es válida.")
        self.__etiqueta = nueva_etiqueta

    def ejecutar_accion(self) -> str:
        return f"Dispositivo {self.id_dispositivo}: Acción genérica ejecutada."

    def detener_accion(self) -> str:
        return f"Dispositivo {self.id_dispositivo}: Acción genérica detenida."
    
    def __str__(self):
        return f"Dispositivo(ID: {self.id_dispositivo}, Etiqueta: {self.etiqueta}, Tipo: {self.id_tipo}, Estado: {self.estado})"
    