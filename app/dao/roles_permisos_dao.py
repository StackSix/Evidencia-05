from __future__ import annotations
from typing import List, Dict, Optional
import mysql.connector
from mysql.connector import Error
from interfaz_dao import DataAccessDAO
from app.conn.cursor import get_cursor
from app.conn.logger import logger
from app.dominio.permisos import Permiso

class RolesPermisosDAO(DataAccessDAO):
    """
    DAO para consultar y gestionar los permisos de un rol.
    Tablas involucradas: rol, permiso, rol_permiso
    """

    # READ: lista de permisos por id_rol
    @staticmethod
    def leer_por_id_rol(id_rol: int) -> List[Permiso]:
        try:
            with get_cursor() as cursor:  # get_cursor ya usa dictionary=True
                query = """
                    SELECT p.id_permiso, p.nombre
                    FROM rol_permiso rp
                    JOIN permiso p ON p.id_permiso = rp.id_permiso
                    WHERE rp.id_rol = %s
                    ORDER BY p.nombre
                """
                cursor.execute(query, (id_rol,))
                rows = cursor.fetchall() or []
                return [Permiso(r["id_permiso"], r["nombre"]) for r in rows]
        except mysql.connector.Error as e:
            logger.exception("❌ No se pudo obtener permisos por id_rol.")
            raise e

    # READ: lista de permisos por nombre de rol
    @staticmethod
    def leer_por_nombre_rol(nombre_rol: str) -> List[Permiso]:
        try:
            with get_cursor() as cursor:
                query = """
                    SELECT p.id_permiso, p.nombre
                    FROM rol r
                    JOIN rol_permiso rp ON rp.id_rol = r.id_rol
                    JOIN permiso p ON p.id_permiso = rp.id_permiso
                    WHERE r.nombre = %s
                    ORDER BY p.nombre
                """
                cursor.execute(query, (nombre_rol,))
                rows = cursor.fetchall() or []
                return [Permiso(r["id_permiso"], r["nombre"]) for r in rows]
        except mysql.connector.Error as e:
            logger.exception("❌ No se pudo obtener permisos por nombre de rol.")
            raise e

    # CREATE: asignar permiso a rol
    @staticmethod
    def asignar_permiso(id_rol: int, id_permiso: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = "INSERT INTO rol_permiso (id_rol, id_permiso) VALUES (%s, %s)"
                cursor.execute(query, (id_rol, id_permiso))
                return cursor.rowcount > 0
        except mysql.connector.IntegrityError:
            # ya existe la relación o FK inválida
            logger.warning("⚠️ La relación rol-permiso ya existe o la FK es inválida.")
            return False
        except mysql.connector.Error as e:
            logger.exception("❌ No se pudo asignar el permiso al rol.")
            raise e

    # DELETE: quitar permiso de rol
    @staticmethod
    def quitar_permiso(id_rol: int, id_permiso: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = "DELETE FROM rol_permiso WHERE id_rol = %s AND id_permiso = %s"
                cursor.execute(query, (id_rol, id_permiso))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("❌ No se pudo quitar el permiso del rol.")
            raise e
