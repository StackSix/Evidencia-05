from typing import List, Optional, Dict
from app.dominio.automatizacion import Automatizacion
from app.dao.automatizaciones_dao import AutomatizacionesDAO

class GestorAutomatizacion:
    """Gestiona la lógica de negocio de las automatizaciones."""

    def __init__(self, automatizaciones: Optional[List[Automatizacion]] = None):
        self.__automatizaciones = automatizaciones if automatizaciones is not None else AutomatizacionesDAO.obtener_todas_activas()

    def registrar(self, automatizacion: Automatizacion, configurar_horario: bool = True) -> None:
        try:
            nuevo_id = AutomatizacionesDAO.registrar_automatizacion(automatizacion)
            print(f"✅ Automatización registrada con ID {nuevo_id}.")
            self.__automatizaciones = AutomatizacionesDAO.obtener_todas_activas()

            # Configuración automática de horario
            if configurar_horario:
                self.__configurar_horario_automatico(nuevo_id)

        except Exception as e:
            print(f"❌ Error al registrar la automatización: {e}")

    def actualizar(self, automatizacion: Automatizacion, configurar_horario: bool = True) -> None:
        try:
            exito = AutomatizacionesDAO.actualizar_automatizacion(automatizacion)
            if exito:
                # actualizar en memoria
                for i, a in enumerate(self.__automatizaciones):
                    if a.id_automatizacion == automatizacion.id_automatizacion:
                        self.__automatizaciones[i] = automatizacion
                        break
                print("✅ Automatización actualizada correctamente.")

                # Configuración automática de horario
                if configurar_horario:
                    self.__configurar_horario_automatico(automatizacion.id_automatizacion)
            else:
                print("❌ No se pudo actualizar la automatización.")
        except Exception as e:
            print(f"❌ Error al actualizar la automatización: {e}")

    def eliminar(self, id_automatizacion: int) -> None:
        try:
            exito = AutomatizacionesDAO.eliminar_automatizacion(id_automatizacion)
            if exito:
                self.__automatizaciones = [a for a in self.__automatizaciones if a.id_automatizacion != id_automatizacion]
                print("✅ Automatización eliminada correctamente.")
            else:
                print("❌ No se pudo eliminar la automatización.")
        except Exception as e:
            print(f"❌ Error al eliminar la automatización: {e}")

    def listar(self, dni_usuario: Optional[int] = None) -> None:
        """
        Lista automatizaciones. Si se pasa dni_usuario, filtra solo domicilios del usuario.
        """
        filtradas = self.__automatizaciones
        if dni_usuario is not None:
            filtradas = [
                a for a in self.__automatizaciones
                if AutomatizacionesDAO.verificar_dueno_de_automatizacion(dni_usuario, a.id_automatizacion)
            ]

        if not filtradas:
            print("❌ No se encontraron automatizaciones.")
            return

        for a in filtradas:
            print(f"{a.id_automatizacion} - Hogar: {a.id_domicilio} - {a.nombre} - {a.accion} - ON: {a.hora_encendido} - OFF: {a.hora_apagado}")

    def obtener_por_id(self, id_automatizacion: int) -> Optional[Automatizacion]:
        for a in self.__automatizaciones:
            if a.id_automatizacion == id_automatizacion:
                return a
        return None

    @property
    def automatizaciones(self) -> List[Automatizacion]:
        return self.__automatizaciones

    def __configurar_horario_automatico(self, id_automatizacion: int) -> None:
        """
        Configura horario automático por defecto: encendido 08:00, apagado 22:00
        """
        automatizacion = AutomatizacionesDAO.obtener_automatizacion(id_automatizacion)
        if not automatizacion:
            print(f"❌ Automatización {id_automatizacion} no encontrada para configurar horario.")
            return

        on = "08:00"
        off = "22:00"

        try:
            automatizacion.configurar_horario(on, off)
            AutomatizacionesDAO.actualizar_automatizacion(automatizacion)
            print(f"⏰ Horario automático configurado para automatización {id_automatizacion}: ON {on} - OFF {off}")
        except Exception as e:
            print(f"❌ Error al configurar horario automático: {e}")
            