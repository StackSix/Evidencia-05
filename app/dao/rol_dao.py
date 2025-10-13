from __future__ import annotations
from typing import Optional, List, Dict
import mysql.connector
from mysql.connector import Error
from app.conn.cursor import get_cursor
from app.conn.logger import logger
from interfaz_dao import DataAccessDAO


class RolDAO(DataAccessDAO):
    """
    DAO para la tabla 'rol'
    """

    # CREATE ----------
    @staticmethod
    def crear(nombre: str) -> int:
        """Crea un nuevo rol en la base de datos y retorna su ID."""
        try:
            with get_cursor(commit=True) as cursor:
                query = "INSERT INTO rol (nombre) VALUES (%s)"
                cursor.execute(query, (nombre,))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("❌ No se pudo registrar el rol en la Base de Datos.")
            raise e

    # READ ----------
    @staticmethod
    def leer(id_rol: int) -> Optional[Dict]:
        """Devuelve un diccionario con la información del rol especificado."""
        try:
            with get_cursor(commit=False) as cursor:
                query = "SELECT id_rol, nombre FROM rol WHERE id_rol = %s"
                cursor.execute(query, (id_rol,))
                result = cursor.fetchone()
                return result
        except mysql.connector.Error as e:
            logger.exception("❌ No se pudo obtener el rol buscado.")
            raise e

    # UPDATE ----------
    @staticmethod
    def actualizar(id_rol: int, nuevo_nombre: str) -> bool:
        """Actualiza el nombre de un rol existente."""
        try:
            with get_cursor(commit=True) as cursor:
                query = "UPDATE rol SET nombre = %s WHERE id_rol = %s"
                cursor.execute(query, (nuevo_nombre, id_rol))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("❌ No se pudo modificar el rol buscado.")
            raise e

    # DELETE ----------
    @staticmethod
    def eliminar(id_rol: int) -> bool:
        """Elimina un rol por ID (solo si no tiene usuarios asociados)."""
        try:
            with get_cursor(commit=True) as cursor:
                query = "DELETE FROM rol WHERE id_rol = %s"
                cursor.execute(query, (id_rol,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("❌ No se pudo eliminar el rol.")
            raise e
