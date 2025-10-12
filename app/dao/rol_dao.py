import mysql.connector
from __future__ import annotations
from typing import Optional, List, Dict
from app.conn.cursor import get_cursor
from mysql.connector import Error
from app.conn.logger import logger
from interfaz_dao import DataAccessDAO
from app.dominio.usuarios import Usuario


class RolDAO(DataAccessDAO):
    "DAO para roles"
    @staticmethod
    def crear(nombre_rol: str)-> int:
        try:
            with get_cursor(commit=True) as cursor:
                query = "INSERT INTO rol (nombre_rol) VALUES (%s)"
                cursor.execute(query, (nombre_rol,))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("No se pudo registrar el rol en la Base de Datos.")
            raise e
    
    @staticmethod
    def leer(id_rol: int)-> Optional[List]:
        try:
            with get_cursor(commit=False) as cursor:
                query = "SELECT nombre_rol FROM rol WHERE id_rol=%s"
                cursor.execute(query, (id_rol,))
                return cursor.fetchone
        except mysql.connector.Error as e:
            logger.exception("No se pudo obtener el rol buscado.")
            raise e 
        
    @staticmethod
    def actualizar(id_rol: int, nombre_rol: str)-> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE rol
                    SET nombre_rol = %s 
                    WHERE id_rol = %s
                """
                cursor.execute(query, (nombre_rol, id_rol))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("No se pudo modificar el rol buscado.")
            raise e 
    
    @staticmethod    
    def eliminar():
        pass
    