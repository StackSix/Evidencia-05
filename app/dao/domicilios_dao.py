"""DAO para operar con domicilios y su vinculación con usuarios."""
from __future__ import annotations
from typing import Dict, List, Any
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
            "INSERT INTO domicilios (direccion, numeracion, ciudad, nombre_domicilio) "
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
    def vincular_usuario(dni: str, hogar_id: int) -> None:
        " Vincula un usuario a un domicilio usando el DNI del usuario. dni: DNI del usuario hogar_id: ID del domicilio (autoincremental)"
        try:
            with get_cursor(commit=True) as cursor:
                # 1️⃣ Buscar el ID real del usuario por su DNI
                cursor.execute("SELECT id FROM usuarios WHERE dni = %s", (dni,))
                row = cursor.fetchone()
                if not row:
                    raise ValueError(f"Usuario con DNI {dni} no existe")
                usuario_id = row[0]

                # 2️⃣ Insertar vínculo en usuarios_hogares
                query = "INSERT IGNORE INTO usuarios_hogares (usuario_id, hogar_id) VALUES (%s, %s)"
                cursor.execute(query, (usuario_id, hogar_id))
                print(f"[DEBUG] Usuario con DNI {dni} (ID {usuario_id}) vinculado al hogar {hogar_id}")

        except mysql.connector.Error as exc:
            logger.exception("No se pudo vincular el usuario al domicilio.")
            raise exc
    
    @staticmethod
    def listar_por_usuario(dni: int) -> List[Dict[str, Any]]:
        """
        Devuelve los domicilios del usuario cuyo DNI = dni.
        Une usuarios (por DNI) -> usuarios_hogares (usuario_id) -> domicilios (hogar_id).
        """
        query = """
            SELECT h.id_hogar,
                   h.nombre_domicilio,
                   h.direccion,
                   h.numeracion,
                   h.ciudad
            FROM usuarios AS u
            JOIN usuarios_hogares AS uh ON uh.usuario_id = u.id
            JOIN domicilios AS h        ON h.id_hogar    = uh.hogar_id
            WHERE u.dni = %s
            ORDER BY h.id_hogar
        """
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query, (dni,))
                return cursor.fetchall()
        except mysql.connector.Error as exc:
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