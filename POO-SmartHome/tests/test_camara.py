import pytest
from camara import Camara, ModoGrabacion
from datetime import datetime

def test_grabar_manual():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.AUTOMATICO, False, False)
    resultado = mycamara.grabar_manual(True)
    assert resultado == 'El modo grabación es AUTOMÁTICO. Cambielo a modo MANUAL e intentelo nuevamente.' 
    
def test_grabar_manual_2():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, False)
    resultado = mycamara.grabar_manual(True)
    assert resultado
    
def test_grabar_manual_3():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, False)
    resultado = mycamara.grabar_manual(False)
    assert resultado
    
def test_grabar_manual_4():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, False)
    with pytest.raises(ValueError):
        mycamara.grabar_manual("asd")
    
def test_modificar_grabacion_modo():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, False)
    result = mycamara.modificar_grabacion_modo(True)
    assert result == "Modo Automático activado."
    
def test_modificar_grabacion_modo_2():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.AUTOMATICO, False, False)
    result = mycamara.modificar_grabacion_modo(False)
    assert result == "Modo Manual activado."
    
def test_grabar_automatico():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.AUTOMATICO, False, False)
    result = mycamara.grabar_automatico()
    assert result == "Automatización apagada"
    assert mycamara._Camara__modo_grabando is False
    
def test_grabar_automatico_2():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.AUTOMATICO, False, True)
    mycamara.hora_encendido = "08:00"
    mycamara.hora_apagado = "23:50"
    resultado = mycamara.grabar_automatico()
    assert resultado == "Cam1 esta grabando"
    assert mycamara._Camara__modo_grabando is True
    
def test_grabar_automatico_3():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, True)
    mycamara.hora_encendido = "23:50"
    mycamara.hora_apagado = "08:00"
    resultado = mycamara.grabar_automatico()
    assert resultado == "Cam1 no esta grabando"
    assert mycamara._Camara__modo_grabando is False
    
def test_procesar_notificacion():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, True)
    # Hora actual = hora_encendido para que pase
    hora_actual = datetime.now().strftime("%H:%M")
    mycamara.hora_encendido = hora_actual
    mycamara.hora_apagado = "23:59"
    mycamara.procesar_notificacion()
    assert mycamara.ultima_notificacion is True
    
def test_procesar_notificacion_2():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, True)
    # Hora actual = hora_encendido para que pase
    hora_actual = datetime.now().strftime("%H:%M")
    mycamara.hora_encendido = "00:01"
    mycamara.hora_apagado = hora_actual
    mycamara.procesar_notificacion()
    assert mycamara.ultima_notificacion is False
    
def test_configurar_automatizacion_horaria():
    mycamara = Camara("camara", "apagado", "Cam1", "M1", ModoGrabacion.MANUAL, False, False)
    resultado = mycamara.configurar_automatizacion_horaria("08:00", "20:00")
    assert resultado == "La camara debe estar encendida."
    assert mycamara.estado_automatizacion is False

def test_configurar_automatizacion_horaria_2():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, False)
    resultado = mycamara.configurar_automatizacion_horaria("08:00", "20:00")
    assert resultado == "Automatización configurada: ON: 08:00 OFF: 20:00"

def test_mostrar_automatizacion():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, False)
    resultado = mycamara.mostrar_automatizacion()
    assert resultado == 'Automatización no configurada.'

def test_mostrar_automatizacion_2():
    mycamara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, True)
    mycamara.hora_encendido = "08:00"
    mycamara.hora_apagado = "20:00"
    resultado = mycamara.mostrar_automatizacion()
    assert resultado == ( f"Automatización configurada. \n" 
            f"Hora de Inicio: 08:00 \n"
            f"Hora de Finalización 20:00 \n" )