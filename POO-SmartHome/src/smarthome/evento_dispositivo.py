class EventoDispositivo:
    contador_id = 0
    def __init__(self):
        EventoDispositivo.contador_id +=1
        self.evento_id = EventoDispositivo.contador_id
        
    def enviar_notificacion(self, evento):
        if not evento:
            return 'El dispositivo dejo de grabar'
        else:
            return 'El dispositivo comenzo a grabar'
        