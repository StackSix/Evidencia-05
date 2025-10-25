from __future__ import annotations
from typing import List, Optional
from datetime import datetime
from app.dominio.automatizacion import Automatizacion
from app.dao.automatizacion_dao import AutomatizacionDAO

class GestorAutomatizacion:
    "Gestiona la lógica de negocio de las automatizaciones."

    def __init__(self, automatizaciones: Optional[List[Automatizacion]] = None):
        self.__automatizaciones = automatizaciones if automatizaciones is not None else AutomatizacionDAO.obtener_todas()

    def registrar(self, automatizacion: Automatizacion) -> None:
        try:
            # Si no se configuró horario, es por defecto este:
            if not automatizacion.hora_encendido or not automatizacion.hora_apagado:
                automatizacion.configurar_horario("08:00", "22:00")

            nuevo_id = AutomatizacionDAO.registrar_automatizacion(automatizacion)
            print(f"✅ Automatización registrada con ID {nuevo_id}.")
            self.__automatizaciones = AutomatizacionDAO.obtener_todas()

        except Exception as e:
            print(f"❌ Error al registrar la automatización: {e}")

    def actualizar(self, automatizacion: Automatizacion, configurar_horario: bool = True) -> None:
        try:
            exito = AutomatizacionDAO.actualizar_automatizacion(automatizacion)
            if exito:
                for i, a in enumerate(self.__automatizaciones):
                    if a.id_automatizacion == automatizacion.id_automatizacion:
                        self.__automatizaciones[i] = automatizacion
                        break
                print("✅ Automatización actualizada correctamente.")

                # Solo configurar horario por defecto si no tiene horarios definidos
                if configurar_horario and (not automatizacion.hora_encendido or not automatizacion.hora_apagado):
                    automatizacion.configurar_horario("08:00", "22:00")
                    AutomatizacionDAO.actualizar_automatizacion(automatizacion)
                
            else:
                print("❌ No se pudo actualizar la automatización.")
        except Exception as e:
            print(f"❌ Error al actualizar la automatización: {e}")

    def eliminar(self, id_automatizacion: int) -> None:
        try:
            exito = AutomatizacionDAO.eliminar_automatizacion(id_automatizacion)
            if exito:
                self.__automatizaciones = [a for a in self.__automatizaciones if a.id_automatizacion != id_automatizacion]
                print("✅ Automatización eliminada correctamente.")
            else:
                print("❌ No se pudo eliminar la automatización.")
        except Exception as e:
            print(f"❌ Error al eliminar la automatización: {e}")

    def listar(self) -> None:
        try:
            automatizaciones = AutomatizacionDAO.obtener_todas()  

            if not automatizaciones:
                print("❌ No se encontraron automatizaciones.")
                return

            print("\n📋 Listado de automatizaciones:")
            for a in automatizaciones:
                estado_txt = "🟢 Activa" if a.estado else "🔴 Inactiva"
                print(f"[{a.id_automatizacion}] {a.nombre} | {a.accion} | Domicilio #{a.id_domicilio} | {estado_txt}")
                print(f"   ⏰ {a.hora_encendido} → {a.hora_apagado}")

        except Exception as e:
            print(f"❌ Error al listar automatizaciones: {e}")
    
    def obtener_por_id(self, id_automatizacion: int) -> Optional[Automatizacion]:
        for a in self.__automatizaciones:
            if a.id_automatizacion == id_automatizacion:
                return a
        return None
    
    @staticmethod
    def pedir_hora(mensaje: str) -> str:
        while True:
            hora_str = input(mensaje)
            try:
                hora_obj = datetime.strptime(hora_str, "%H:%M")
                return hora_obj.strftime("%H:%M")
            except:
                print("Debe ingresar un horario valido. HH:MM")

    @property
    def automatizaciones(self) -> List[Automatizacion]:
        return self.__automatizaciones
