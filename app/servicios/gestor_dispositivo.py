from typing import List, Optional
from app.dominio.dispositivos import Dispositivo
from app.dao.dispositivos_dao import DispositivoDAO

class GestorDispositivo:
    """
    Gestiona la lógica de negocio de los dispositivos de un domicilio,
    utilizando un DAO para la persistencia.
    """
    def __init__(self, id_domicilio: int):
        self.__id_domicilio = id_domicilio
        self.__dispositivos_dao = DispositivoDAO()
        self.__dispositivos = self.__dispositivos_dao.listar_dispositivos_por_domicilio(id_domicilio)

    def agregar_dispositivo(self, etiqueta: str, id_tipo: int) -> None:
        try:
            id_nuevo = self.__dispositivos_dao.registrar_dispositivo(self.__id_domicilio, id_tipo, etiqueta)
            if id_nuevo:
                self.__dispositivos = self.__dispositivos_dao.listar_dispositivos_por_domicilio(self.__id_domicilio)
                print("✅ Dispositivo agregado correctamente.")
            else:
                print("❌ No se pudo agregar el dispositivo.")
        except Exception as e:
            print(f"❌ Error al agregar el dispositivo: {e}")

    def eliminar_dispositivo(self, id_dispositivo: int) -> None:
        dispositivo_a_eliminar = self.obtener_dispositivo(id_dispositivo)
        if not dispositivo_a_eliminar:
            print("⚠️ Dispositivo no encontrado en este domicilio.")
            return
        try:
            self.__dispositivos_dao.eliminar_dispositivo(id_dispositivo)
            self.__dispositivos = self.__dispositivos_dao.listar_dispositivos_por_domicilio(self.__id_domicilio)
            print("✅ Dispositivo eliminado correctamente.")
        except Exception as e:
            print(f"❌ Error al eliminar el dispositivo: {e}")

    def actualizar_dispositivo(self, id_dispositivo: int, *, id_domicilio: Optional[int] = None, id_tipo: Optional[int] = None, etiqueta: Optional[str] = None) -> None:
        dispositivo_existente = self.obtener_dispositivo(id_dispositivo)
        if not dispositivo_existente:
            print("⚠️ Dispositivo no encontrado en este domicilio.")
            return
        try:
            self.__dispositivos_dao.actualizar_dispositivo(
                id_dispositivo,
                id_domicilio=id_domicilio,
                id_tipo=id_tipo,
                etiqueta=etiqueta
            )
            self.__dispositivos = self.__dispositivos_dao.listar_dispositivos_por_domicilio(self.__id_domicilio)
            print("✅ Dispositivo actualizado correctamente.")
        except Exception as e:
            print(f"❌ Error al actualizar el dispositivo: {e}")

    def obtener_dispositivo(self, id_dispositivo: int) -> Optional[Dispositivo]:
        for d in self.__dispositivos:
            if d.id_dispositivo == id_dispositivo:
                return d
        return None

    def listar_dispositivos(self) -> None:
        if not self.__dispositivos:
            print(f"No hay dispositivos cargados en este domicilio.")
        else:
            print(f"\n--- Dispositivos en domicilio {self.__id_domicilio} ---")
            for d in self.__dispositivos:
                estado_str = "Encendido" if d.estado else "Apagado"
                print(f"- ID: {d.id_dispositivo} | Etiqueta: {d.etiqueta} | Tipo: {d.id_tipo} | Estado: {estado_str}")

    @property
    def dispositivos(self) -> List[Dispositivo]:
        return self.__dispositivos
    