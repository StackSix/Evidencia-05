class Dispositivo:
    _contador_id = 0
    def __init__(self, tipo, estado_dispositivo):
        Dispositivo._contador_id += 1
        self.__id = Dispositivo._contador_id
        self.__tipo = tipo
        self.__estado_dispositivo = estado_dispositivo
    
    @property
    def id(self):
        return self.__id
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def estado_dispositivo(self):
        return self.__estado_dispositivo
        
    def __str__(self):
        return f'Datos del Dispositivo: ID: {self.id} Tipo: {self.tipo} Estado: {self.estado_dispositivo}'
    
    def modificar_estado_dispositivo(self, nuevo_estado):
        if nuevo_estado in ["encendido", "apagado"]:
            self.__estado_dispositivo = nuevo_estado
            return self.__estado_dispositivo
        else:
            return "Debe ingresar una opción válida"
        