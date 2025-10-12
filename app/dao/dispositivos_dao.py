"""Acceso a datos para dispositivos vinculados a la plataforma SmartHome."""
from __future__ import annotations

from typing import Any, Dict, List, Optional 

import mysql.connector

from app.conn.cursor import get_cursor
from app.conn.logger import logger


class DispositivoDAO:
    """DAO con operaciones básicas sobre la tabla ``dispositivos``."""

    @staticmethod
    def crear_dispositivo(
        id_habitacion: Optional[int],
        id_tipo: int,
        estado: bool,
        etiqueta: str,
    ) -> int:
        """Crea un dispositivo y devuelve su identificador."""

        query = (
            "INSERT INTO dispositivos (id_habitacion, id_tipo, estado, etiqueta) "
            "VALUES (%s, %s, %s, %s)"
        )
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (id_habitacion, id_tipo, estado, etiqueta))
                return cursor.lastrowid
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("Error al intentar crear el dispositivo.")
            raise exc

    @staticmethod
    def obtener_por_usuario(usuario_id: int) -> List[Dict[str, Any]]:
        """Obtiene los dispositivos asociados al usuario mediante sus domicilios."""

        query = (
            "SELECT d.id, d.id_habitacion, d.id_tipo, d.estado, d.etiqueta "
            "FROM dispositivos AS d "
            "JOIN habitaciones AS h ON h.id = d.id_habitacion "
            "JOIN usuarios_domicilios AS ud ON ud.id_hogar = h.id_hogar "
            "JOIN usuarios AS u ON u.dni = ud.dni "
            "WHERE u.id = %s ORDER BY d.id"
        )
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query, (usuario_id,))
                return cursor.fetchall()
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("Error al listar los dispositivos del usuario.")
            raise exc

    @staticmethod
    def actualizar(dispositivo_id: int, **campos: Any) -> None:
        """Actualiza los campos indicados para un dispositivo."""

        if not campos:
            return

        columnas: List[str] = []
        valores: List[Any] = []
        for columna, valor in campos.items():
            columnas.append(f"{columna} = %s")
            valores.append(valor)
        valores.append(dispositivo_id)

        query = f"UPDATE dispositivos SET {', '.join(columnas)} WHERE id = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, tuple(valores))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("Error al actualizar el dispositivo %s", dispositivo_id)
            raise exc

    @staticmethod
    def eliminar(dispositivo_id: int) -> None:
        query = "DELETE FROM dispositivos WHERE id = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (dispositivo_id,))
        except mysql.connector.Error as exc:  # pragma: no cover - solo log
            logger.exception("Error al eliminar el dispositivo %s", dispositivo_id)
            raise exc