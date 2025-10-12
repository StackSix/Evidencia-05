"""DAO encargado de la tabla ``tipo_habitacion``."""
from __future__ import annotations

from typing import Dict, List

import mysql.connector

from app.conn.cursor import get_cursor
from app.conn.logger import logger


class TipoHabitacionDAO:
    @staticmethod
    def crear(id_hogar: int, nombre_habitacion: str) -> int:
        query = "INSERT INTO tipo_habitacion (id_hogar, nombre_habitacion) VALUES (%s, %s)"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (id_hogar, nombre_habitacion))
                return cursor.lastrowid
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo crear la habitación.")
            raise exc

    @staticmethod
    def listar_por_hogar(id_hogar: int) -> List[Dict]:
        query = (
            "SELECT id_habitacion, nombre_habitacion FROM tipo_habitacion "
            "WHERE id_hogar = %s ORDER BY id_habitacion"
        )
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query, (id_hogar,))
                return cursor.fetchall()
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudieron recuperar las habitaciones del hogar.")
            raise exc

    @staticmethod
    def modificar_nombre(id_habitacion: int, nuevo_nombre: str) -> None:
        query = "UPDATE tipo_habitacion SET nombre_habitacion = %s WHERE id_habitacion = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (nuevo_nombre, id_habitacion))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo actualizar la habitación %s", id_habitacion)
            raise exc

    @staticmethod
    def eliminar(id_habitacion: int) -> None:
        query = "DELETE FROM tipo_habitacion WHERE id_habitacion = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (id_habitacion,))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo eliminar la habitación %s", id_habitacion)
            raise exc