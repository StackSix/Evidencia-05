"""Servicios para la gestión de domicilios utilizando el DAO remoto."""
from __future__ import annotations

from typing import Dict, List

from app.dao.domicilios_dao import DomicilioDAO


class DomiciliosService:
    @staticmethod
    def listar_por_usuario(dni: int):
        hogares = DomicilioDAO.listar_por_usuario(dni)
        if not hogares:
            print("⚠️  No tienes domicilios registrados aún.")
            return []
        print("\n🏠 Tus domicilios registrados:")
        for h in hogares:
            print(f" - {h['nombre_domicilio']} ({h['direccion']} {h['numeracion']}, {h['ciudad']})")
        return hogares

    @staticmethod
    def crear(dni: int, direccion: str, numeracion: str, ciudad: str, alias: str) -> int:
        hogar_id = DomicilioDAO.crear_domicilio(direccion, numeracion, ciudad, alias)
        DomicilioDAO.vincular_usuario(dni, hogar_id)
        return hogar_id

    @staticmethod
    def actualizar(
        id_hogar: int,
        direccion: str,
        numeracion: str,
        ciudad: str,
        alias: str,
    ) -> None:
        DomicilioDAO.actualizar_domicilio(id_hogar, direccion, numeracion, ciudad, alias)

    @staticmethod
    def eliminar(id_hogar: int) -> None:
        DomicilioDAO.eliminar(id_hogar)