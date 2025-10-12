from dispositivos import Dispositivo

class Camara(Dispositivo):
    "Clase para dispositivos de tipo Cámara."
    def __init__(self, id_dispositivo: int, id_habitacion: int, nombre_camara: str, grabacion_modo: str, estado_automatizacion: bool, estado: str):
        super().__init__("grabar", id_dispositivo, id_habitacion, estado)
        self.nombre_camara = nombre_camara
        self.grabacion_modo = grabacion_modo
        self.estado_automatizacion = estado_automatizacion
        
    def ejecutar_accion(self) -> str:
        self.cambiar_estado("grabando")
        return f"Cámara {self.id_dispositivo}: Grabación iniciada."
    
    def detener_accion(self) -> str:
        self.cambiar_estado("detenida")
        return f"Cámara {self.id_dispositivo}: Grabación detenida."
    