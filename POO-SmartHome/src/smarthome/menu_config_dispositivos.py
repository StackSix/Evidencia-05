from camara import Camara, ModoGrabacion
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def pedir_hora(mensaje):
    while True:
        hora_str = input(mensaje).strip()
        try:
            hora_obj = datetime.strptime(hora_str, "%H:%M")
            return hora_obj.strftime("%H:%M")
        except:
            print("Debe ingresar un horario valido. HH:MM en un rango de 00:00 a 23:59")
            
def menu_dispositivo(camara: Camara):
    while True:
        print("\n--- Configuración de su Dispositivo ---")
        if camara.estado_dispositivo == 'encendido':
            print("1. Apagar Dispositivo ")
        else:
            print("1. Encender Dispositivo ")
        print("2. Ver Datos del Dispositivo")
        print("3. Grabación Manual")
        print("4. Modificar Modo de Grabación")
        print("5. Configurar Automatización Horaria")
        print("6. Mostrar Automatización")
        print("7. Ver Estado de Grabación")
        print("8. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            if not camara.estado_dispositivo == 'apagado':
                nuevo_estado = input("Para modificar el estado a apagado ingrese (apagado): ")
                try:
                    camara.modificar_estado_dispositivo(nuevo_estado)
                    logger.info(f"{camara.nombre}: Se apagó el dispositivo.")
                except ValueError as e:
                    print(f"Error: {e}")

            else:
                nuevo_estado = input("Para modificar el estado a encendido ingrese (encendido): ")
                try:    
                    camara.modificar_estado_dispositivo(nuevo_estado)
                    logger.info(f"{camara.nombre}: Se encendió el dispositivo.")
                except ValueError as e:
                    print(f"Error: {e}")
                
        elif opcion == "2":
            print("\n",camara)
        
        elif opcion == "3":    
            if camara.estado_dispositivo != "encendido":
                print(f"{camara.nombre}: No se puede grabar, el dispositivo está apagado.")
            else:
                rec = not camara.modo_grabando
                camara.grabar_manual(rec)

        elif opcion == "4":
            if camara.grabacion_modo == ModoGrabacion.MANUAL:
                if not camara.estado_automatizacion:
                    print("No se puede cambiar a modo de grabación automatico porque no hay una automatización configurada.")
                    logger.warning(f"{camara.nombre}: Se intento cambiar a modo automático sin tener configurada una automatización.")
                else:
                    modo = camara.modificar_grabacion_modo(True)
                    encendido_automatico = camara.grabar_automatico()
                    logger.info(f"{camara.nombre}: Se cambió con éxito el modo de grabación")
                    print("El modo se modificó con éxito.")
                    print(modo)
                    print(encendido_automatico)
            else:
                camara.modificar_grabacion_modo(False)
                logger.info(f"{camara.nombre}: Se cambió con éxito el modo de grabación")
                print("El modo se modificó con éxito.")
                
        elif opcion == "5":
            print("Ingrese su configuración horaria (HH:MM): \n")
            on = pedir_hora("Horario de Encendido: ")
            off = pedir_hora("Horario de Apagado: ")
            configuracion = camara.configurar_automatizacion_horaria(on, off)
            automatizacion_inicial = camara.grabar_automatico()
            notificacion = camara.procesar_notificacion()
            print(configuracion)
            print(automatizacion_inicial)
            print(notificacion)
        
        elif opcion == "6":
            print("\n",camara.mostrar_automatizacion())
            
        elif opcion == "7":
            if camara.modo_grabando:
                print(f"{camara.nombre}: Esta Grabando.")
            else:
                print(f"{camara.nombre}: No esta Grabando") 
            
        elif opcion == "8":
            print("Cerrando Configuración.")
            break
        
        else:
            print("Debe ingresar una opción válida. Intentelo nuevamente.")


if __name__ == "__main__":
    camara = Camara("camara", "encendido", "Cam1", "M1", ModoGrabacion.MANUAL, False, False)
    menu_dispositivo(camara)