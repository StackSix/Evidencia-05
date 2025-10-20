from __future__ import annotations
from typing import List, Optional
from app.dominio.domicilio import Domicilio
from app.dao.domicilios_dao import DomiciliosDAO

class GestorDomicilio:
    """
    Gestiona la lógica de negocio de los domicilios, manteniendo una lista en memoria
    y sincronizando con la base de datos mediante el DAO.
    """
    def __init__(self, domicilios: Optional[List[Domicilio]] = None):
        self.__domicilios = domicilios if domicilios is not None else []

    def agregar_domicilio(self, direccion: str, numeracion: str, ciudad: str, nombre_domicilio: str) -> None:
        try:
            id_domicilio = DomiciliosDAO.registrar_domicilio(direccion, numeracion, ciudad, nombre_domicilio)
            nuevo_domicilio = Domicilio(
                id_domicilio=id_domicilio,
                direccion=direccion,
                ciudad=ciudad,
                nombre_domicilio=nombre_domicilio
            )
            self.__domicilios.append(nuevo_domicilio)
            print(f"✅ Domicilio registrado correctamente con ID: {id_domicilio}")
        except Exception as e:
            print(f"❌ Error al registrar el domicilio: {e}")

    def eliminar_domicilio(self, id_domicilio: int) -> None:
        try:
            eliminado = DomiciliosDAO.eliminar_domicilio(id_domicilio)
            if eliminado:
                self.__domicilios = [d for d in self.__domicilios if d.id_domicilio != id_domicilio]
                print("✅ Domicilio eliminado correctamente.")
            else:
                print("❌ No se encontró el domicilio.")
        except Exception as e:
            print(f"❌ Error al eliminar el domicilio: {e}")

    def actualizar_domicilio(self, id_domicilio: int, direccion: str, numeracion: str, ciudad: str, nombre_domicilio: str) -> None:
        try:
            actualizado = DomiciliosDAO.actualizar_domicilio(id_domicilio, direccion, numeracion, ciudad, nombre_domicilio)
            if actualizado:
                domicilio = self.obtener_domicilio(id_domicilio)
                if domicilio:
                    domicilio.direccion = direccion
                    domicilio.ciudad = ciudad
                    domicilio.nombre_domicilio = nombre_domicilio
                print("✅ Domicilio actualizado correctamente.")
            else:
                print("❌ No se encontró el domicilio o no hubo cambios.")
        except Exception as e:
            print(f"❌ Error al actualizar el domicilio: {e}")

    def obtener_domicilio(self, id_domicilio: int) -> Optional[Domicilio]:
        for d in self.__domicilios:
            if d.id_domicilio == id_domicilio:
                return d
        return None

    def listar_domicilios(self) -> None:
        if not self.__domicilios:
            print("❌ No hay domicilios registrados.")
        else:
            print("\n--- Domicilios registrados ---")
            for d in self.__domicilios:
                print(f"- ID: {d.id_domicilio} | {d.nombre_domicilio} | {d.direccion} ({d.ciudad})")

    @property
    def domicilios(self) -> List[Domicilio]:
        return self.__domicilios
