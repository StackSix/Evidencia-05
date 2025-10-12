from dispositivos import Dispositivo

class Camara(Dispositivo):
    "Clase para dispositivos de tipo Cámara."
    def __init__(self, id_dispositivo: int, id_habitacion: int, nombre_camara: str, grabacion_modo: str, estado_automatizacion: bool, accion: str, estado: str):
        super().__init__(accion, id_dispositivo, id_habitacion, estado)
        self.nombre_camara = nombre_camara
        self.grabacion_modo = grabacion_modo
        self.estado_automatizacion = estado_automatizacion
        
    def ejecutar_accion(self, accion: str) -> str:
        if accion == "grabar":
            self.estado = "grabando"
            return f"Cámara {self.id_dispositivo}: Grabación iniciada."
        return f"Cámara {self.id_dispositivo}: Acción '{accion}' no soportada."

    def detener_accion(self, accion: str) -> str:
        if accion == "grabar":
            self.estado = "detenida"
            return f"Cámara {self.id_dispositivo}: Grabación detenida."
        return f"Cámara {self.id_dispositivo}: Acción '{accion}' no soportada."