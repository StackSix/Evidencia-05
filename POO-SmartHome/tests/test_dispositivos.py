from dispositivos import Dispositivo

def test_modificar_estado_dispositivo_1():
    my_dispositivo = Dispositivo("camara", "apagado")
    assert my_dispositivo.modificar_estado_dispositivo("apagado") == "apagado"

def test_modificar_estado_dispositivo_2():
    my_dispositivo = Dispositivo("camara", "encendido")
    assert my_dispositivo.modificar_estado_dispositivo("encendido") == "encendido"
    
def test_modificar_estado_dispositivo_3():
    my_dispositivo = Dispositivo("camara", "encendido")
    assert my_dispositivo.modificar_estado_dispositivo("Cualquier palabra") == "Debe ingresar una opción válida"
    
def test_modificar_estado_dispositivo_4():
    my_dispositivo = Dispositivo("camara", "encendido")
    assert my_dispositivo.modificar_estado_dispositivo(False) == "Debe ingresar una opción válida"
    