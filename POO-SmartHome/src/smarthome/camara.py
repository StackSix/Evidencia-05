from dispositivos import Dispositivo
from controlautomatizacion import ControlAutomatizacion
from datetime import datetime
from evento_dispositivo import EventoDispositivo

class Camara(Dispositivo, ControlAutomatizacion):
    def __init__(self, tipo, estado_dispositivo, nombre, modelo, grabacion_modo=None, modo_grabando=False, estado_automatizacion=False):
        super().__init__(tipo, estado_dispositivo)
        self.__nombre = nombre
        self.__modelo = modelo
        self.__grabacion_modo = grabacion_modo
        self.__modo_grabando = modo_grabando
        self.__estado_automatizacion = estado_automatizacion
        self.hora_encendido = None
        self.hora_apagado = None
        
    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre
        return self.__nombre
    
    @property
    def modelo(self):
        return self.__modelo
    
    @modelo.setter
    def modelo(self, nuevo_modelo):
        self.__modelo = nuevo_modelo
    
    @property
    def grabacion_modo(self):
        return self.__grabacion_modo
    
    @grabacion_modo.setter
    def grabacion_modo(self, grabacion_modo):
        self.__grabacion_modo = grabacion_modo
        return self.__grabacion_modo
    
    @property
    def modo_grabando(self):
        return self.__modo_grabando
    
    @property
    def estado_automatizacion(self):
        return self.__estado_automatizacion
    
    @estado_automatizacion.setter
    def estado_automatizacion(self, estado_automatizacion):
        self.__estado_automatizacion = estado_automatizacion
        return self.__estado_automatizacion
    
    def __str__(self):
        return super().__str__() + f"Nombre: {self.nombre} Modelo: {self.modelo} Grabacion Modo: {self.grabacion_modo} Automatización: {self.estado_automatizacion}"
    
    def grabar_manual(self, rec):
        if not self.grabacion_modo == "Manual":
            return 'El modo grabación es AUTOMÁTICO. Cambielo a modo MANUAL e intentelo nuevamente.' 

        if not isinstance(rec, bool):
            return 'Error. Debe ingresar una opción válida.' 
        
        if rec:
            self.__modo_grabando = True
            return "Grabando"
        
        else:
            self.__modo_grabando = False
            return "Guardando"
        
    def modificar_grabacion_modo(self, mode):
        if not isinstance(mode, bool):
            return "Error. Debe ingresar una opción válida."
        
        if not mode:
            self.__grabacion_modo = "Manual"
            return 'Modo MANUAL Activado' 
    
        else:
            self.__grabacion_modo = "Automático"
            return 'Modo Automatico Activado'
        
    def grabar_automatico(self):
        if not self.estado_automatizacion:
            self.__modo_grabando = False
            return 'Automatización apagada'
        
        hora_str = datetime.now().strftime("%H:%M")
        if self.hora_encendido <= hora_str < self.hora_apagado:
            self.__modo_grabando = True
            return f'{self.nombre} esta grabando'        
    
        else:
            self.__modo_grabando = False
            return f'{self.nombre} no esta grabando'
        
    def procesar_notificacion(self):
        hora_str = datetime.now().strftime("%H:%M")
        notificacion = EventoDispositivo()
        if hora_str == self.hora_encendido:
            notificacion.enviar_notificacion(True)
            self.ultima_notificacion = True
            
        elif hora_str == self.hora_apagado:
            notificacion.enviar_notificacion(False)     
            self.ultima_notificacion = False
    
    def configurar_automatizacion_horaria(self, on, off):
        if not self.estado_dispositivo == "encendido":
            return "La camara debe estar encendida."

        else:
            self.estado_automatizacion = True
            self.hora_encendido = on
            self.hora_apagado = off
            return f'Automatización configurada: ON: {on} OFF: {off}'

    def mostrar_automatizacion(self):
        if not self.estado_automatizacion:
            return 'Automatización no configurada.'
        else:
            return f'Automatización configurada. Hora de Inicio: {self.hora_encendido} Hora de Finalización {self.hora_apagado}' 
    