import sys
import os
from smarthome.evento_dispositivo import EventoDispositivo

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_enviar_notificacion():
    evento = EventoDispositivo()
    resultado = evento.enviar_notificacion(False)
    assert resultado

def test_enviar_notificacion_2():
    evento = EventoDispositivo()
    resultado = evento.enviar_notificacion(True)
    assert resultado
    