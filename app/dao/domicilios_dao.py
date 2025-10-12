"""DAO para operar con domicilios y su vinculación con usuarios."""
from __future__ import annotations

from typing import Dict, List

import mysql.connector

from app.conn.cursor import get_cursor
from app.conn.logger import logger


class DomicilioDAO:
    @staticmethod
    def crear_domicilio(
        direccion: str,
        numeracion: str,
        ciudad: str,
        nombre_domicilio: str,
    ) -> int:
        query = (
            "INSERT INTO domicilios (direccion, numeracion, ciudad, alias_domicilio) "
            "VALUES (%s, %s, %s, %s)"
        )
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (direccion, numeracion, ciudad, nombre_domicilio))
                return cursor.lastrowid
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo registrar el domicilio.")
            raise exc

    @staticmethod
    def vincular_usuario(dni: int, id_hogar: int) -> None:
        query = "INSERT IGNORE INTO usuarios_domicilios (dni, id_hogar) VALUES (%s, %s)"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (dni, id_hogar))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo vincular el usuario al domicilio.")
            raise exc

    @staticmethod
    def listar_por_usuario(dni: int) -> List[Dict]:
        query = (
            "SELECT h.id_hogar, h.alias_domicilio, h.direccion, h.numeracion, h.ciudad "
            "FROM usuarios_domicilios AS uh "
            "JOIN domicilios AS h ON h.id_hogar = uh.id_hogar "
            "WHERE uh.dni = %s ORDER BY h.id_hogar"
        )
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query, (dni,))
                return cursor.fetchall()
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("Error al recuperar los domicilios del usuario.")
            raise exc

    @staticmethod
    def actualizar_domicilio(
        id_hogar: int,
        direccion: str,
        numeracion: str,
        ciudad: str,
        nombre_domicilio: str,
    ) -> None:
        query = (
            "UPDATE domicilios SET direccion = %s, numeracion = %s, ciudad = %s, alias_domicilio = %s "
            "WHERE id_hogar = %s"
        )
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (direccion, numeracion, ciudad, nombre_domicilio, id_hogar))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo actualizar el domicilio %s", id_hogar)
            raise exc

    @staticmethod
    def eliminar(id_hogar: int) -> None:
        query = "DELETE FROM domicilios WHERE id_hogar = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (id_hogar,))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("No se pudo eliminar el domicilio %s", id_hogar)