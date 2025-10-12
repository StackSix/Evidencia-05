import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Optional
from app.conn.cursor import get_cursor
from interfaz_dao import DataAccessDAO
from app.conn.logger import logger

class DomiciliosDAO(DataAccessDAO):
    @staticmethod
    def crear(direccion: str, numeracion: str, ciudad: str, alias_domicilio: str)-> int:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO domicilios (direccion, numeracion, ciudad, alias_domicilio)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (direccion, numeracion, ciudad, alias_domicilio))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("Error al intentar registrar domicilio.")
            raise e

    @staticmethod
    def vincular_usuario(dni: int, id_hogar: int)-> None:
        try:
            with get_cursor(commit=True) as cursor:
                query = "INSERT IGNORE INTO usuarios_domicilios (dni, id_hogar) VALUES (%s, %s)"
                cursor.execute(query, (dni, id_hogar))
        except mysql.connector.Error as e:
            logger.exception("No se pudo vincular el usuario con el domicilio.")
            raise e
            
    @staticmethod
    def leer(dni: int)-> Optional[List[Dict]]:
        try:
            with get_cursor(commit=False) as cursor:
                query = """
                    SELECT h.id_hogar, h.nombre_domicilio, h.direccion, h.ciudad
                    FROM usuarios_domicilios uh
                    JOIN domicilios h ON h.id_hogar = uh.id_hogar
                    WHERE uh.dni = %s
                    ORDER BY h.id_hogar
                """
                cursor.execute(query, (dni,))
                rows = cursor.fetchall()
                return rows
        except mysql.connector.Error as e:
            logger.exception("Error al intentar recuperar los datos del usuario y su domicilio.")
            raise e
    
    @staticmethod
    def actualizar(id_hogar: int, direccion: str, numeracion: str, ciudad: str, alias_domicilio: str)-> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE domicilios
                    SET direccion=%s, numeracion=%s, ciudad=%s, alias_domicilio=%s
                    WHERE id_hogar=%s
                """
                cursor.execute(query, (id_hogar, direccion, numeracion, ciudad, alias_domicilio))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar modificar datos del domicilio.")
            raise e
        
    @staticmethod
    def eliminar(id_hogar: int)-> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = "DELETE FROM domicilios WHERE id_hogar=%s"
                cursor.execute(query, (id_hogar,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar eliminar el domicilio.")
            raise e