"""DAO para la gestión de automatizaciones en la base remota."""
from __future__ import annotations

from typing import Dict, List, Optional

import mysql.connector

from app.conn.cursor import get_cursor
from app.conn.logger import logger


class AutomatizacionDAO:
    @staticmethod
    def crear_automatizacion(
        id_hogar: int,
        nombre: str,
        accion: str,
        dias: str,
        hora: str,
        activa: bool,
    ) -> int:
        query = (
            "INSERT INTO automatizaciones (id_hogar, nombre, accion, dias, hora, activa) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (id_hogar, nombre, accion, dias, hora, activa))
                return cursor.lastrowid
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo registrar la automatización.")
            raise exc

    @staticmethod
    def obtener_por_id(automatizacion_id: int) -> Optional[Dict]:
        query = (
            "SELECT id_automatizacion, id_hogar, nombre, accion, dias, hora, activa "
            "FROM automatizaciones WHERE id_automatizacion = %s"
        )
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query, (automatizacion_id,))
                return cursor.fetchone()
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo recuperar la automatización solicitada.")
            raise exc

    @staticmethod
    def listar() -> List[Dict]:
        query = "SELECT id_automatizacion, id_hogar, nombre, accion, dias, hora, activa FROM automatizaciones ORDER BY id_automatizacion"
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudieron listar las automatizaciones.")
            raise exc

    @staticmethod
    def actualizar(
        automatizacion_id: int,
        *,
        id_hogar: Optional[int] = None,
        nombre: Optional[str] = None,
        accion: Optional[str] = None,
        dias: Optional[str] = None,
        hora: Optional[str] = None,
        activa: Optional[bool] = None,
    ) -> None:
        campos: Dict[str, object] = {}
        if id_hogar is not None:
            campos["id_hogar"] = id_hogar
        if nombre is not None:
            campos["nombre"] = nombre
        if accion is not None:
            campos["accion"] = accion
        if dias is not None:
            campos["dias"] = dias
        if hora is not None:
            campos["hora"] = hora
        if activa is not None:
            campos["activa"] = activa

        if not campos:
            return

        sets = ", ".join(f"{col} = %s" for col in campos)
        valores = list(campos.values())
        valores.append(automatizacion_id)

        query = f"UPDATE automatizaciones SET {sets} WHERE id_automatizacion = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, tuple(valores))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception(
                "No se pudo actualizar la automatización con id %s", automatizacion_id
            )
            raise exc

    @staticmethod
    def eliminar(automatizacion_id: int) -> None:
        query = "DELETE FROM automatizaciones WHERE id_automatizacion = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (automatizacion_id,))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo eliminar la automatización %s", automatizacion_id)
            raise exc