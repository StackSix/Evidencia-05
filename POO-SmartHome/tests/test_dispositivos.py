import pytest
from dispositivos import Dispositivo

def test_modificar_estado_dispositivo_1():
    my_dispositivo = Dispositivo("camara", "apagado")
    resultado = my_dispositivo.modificar_estado_dispositivo("apagado")
    assert resultado == "apagado"

def test_modificar_estado_dispositivo_2():
    my_dispositivo = Dispositivo("camara", "encendido")
    resultado = my_dispositivo.modificar_estado_dispositivo("encendido")
    assert resultado == "encendido"
    
def test_modificar_estado_dispositivo_3():
    my_dispositivo = Dispositivo("camara", "encendido")
    with pytest.raises(ValueError):
        my_dispositivo.modificar_estado_dispositivo(True) 
        