"""Servicios de habitaciones apoyados en ``TipoHabitacionDAO``."""
from __future__ import annotations
from typing import Dict, List
from app.dao.habitacion_dao import TipoHabitacionDAO


class HabitacionService:
    @staticmethod
    def listar_por_hogar(id_hogar: int) -> List[Dict]:
        return TipoHabitacionDAO.listar_por_hogar(id_hogar)

    @staticmethod
    def crear(id_hogar: int, nombre: str) -> int:
        return TipoHabitacionDAO.crear(id_hogar, nombre)

    @staticmethod
    def renombrar(id_habitacion: int, nuevo_nombre: str) -> None:
        TipoHabitacionDAO.modificar_nombre(id_habitacion, nuevo_nombre)

    @staticmethod
    def eliminar(id_habitacion: int) -> None:
        TipoHabitacionDAO.eliminar(id_habitacion)