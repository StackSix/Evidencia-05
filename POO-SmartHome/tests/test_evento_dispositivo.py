from evento_dispositivo import EventoDispositivo

def test_enviar_notificacion():
    evento = EventoDispositivo()
    resultado = evento.enviar_notificacion(False)
    assert resultado

def test_enviar_notificacion_2():
    evento = EventoDispositivo()
    resultado = evento.enviar_notificacion(True)
    assert resultado
    