import time
from app.dao.automatizaciones_dao import AutomatizacionesDAO
from app.dao.dispositivos_dao import DispositivoDAO
from datetime import datetime

def monitorizar_automatizaciones():
    print("Iniciando monitor de automatizaciones en la consola...")
    print("Presiona Ctrl+C para detener.")
    try:
        while True:
            automatizaciones_activas = AutomatizacionesDAO.leer_todas_activas()
            
            for automatizacion in automatizaciones_activas:
                # La lógica que ya definiste en el servicio
                if not (automatizacion.hora_encendido and automatizacion.hora_apagado):
                    continue
                
                hora_actual = datetime.now().strftime("%H:%M")
                esta_en_horario = False
                
                if automatizacion.hora_encendido <= automatizacion.hora_apagado:
                    if automatizacion.hora_encendido <= hora_actual < automatizacion.hora_apagado:
                        esta_en_horario = True
                else:
                    if hora_actual >= automatizacion.hora_encendido or hora_actual < automatizacion.hora_apagado:
                        esta_en_horario = True
                
                dispositivo_asociado = DispositivoDAO.leer(automatizacion.id_dispositivo_asociado)
                if not dispositivo_asociado:
                    continue
                
                if esta_en_horario:
                    print(f"[{hora_actual}] Ejecutando acción para automatización ID: {automatizacion.id_automatizacion}")
                    dispositivo_asociado.ejecutar_accion()
                else:
                    print(f"[{hora_actual}] Deteniendo acción para automatización ID: {automatizacion.id_automatizacion}")
                    dispositivo_asociado.detener_accion()
            
            time.sleep(60) # Pausar la ejecución durante 60 segundos

    except KeyboardInterrupt:
        print("\nMonitor de automatizaciones detenido por el usuario.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    