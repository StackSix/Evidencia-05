from typing import List, Dict
from app.conn.cursor import get_cursor
import mysql.connector
from mysql.connector import Error
from app.conn.logger import logger

class HabitacionDAO:
    @staticmethod
    def crear(id_hogar: int, nombre_habitacion: str)-> int:
        try:
            with get_cursor(commit=True) as cursor:
                query = "INSERT INTO tipo_habitacion (id_hogar, nombre_habitacion) VALUES (%s, %s)"
                cursor.execute(query, (id_hogar, nombre_habitacion))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("Error al intentar registrar la habitacion.")
            raise e

    @staticmethod
    def leer(id_hogar: int)-> List[Dict]:
        try:
            with get_cursor(commit=False) as cursor:
                query = """
                    SELECT id_habitacion, nombre_habitacion 
                    FROM tipo_habitacion 
                    WHERE id_hogar = %s ORDER BY id_habitacion
                """
                cursor.execute(query, (id_hogar,))
                rows = cursor.fetchall()
                return rows
        except mysql.connector.Error as e:
            logger.exception("Error al intentar recuperar las habitaciones del domicilio.")
            raise e
    
    @staticmethod
    def actualizar(id_habitacion: int, nombre_habitacion: str)-> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE tipo_habitacion
                    SET nombre_habitacion=%s
                    WHERE id_habitacion=%s
                """
                cursor.execute(query, (nombre_habitacion, id_habitacion))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar modificar datos de la habitacion.")
            raise e
        
    @staticmethod
    def eliminar(id_habitacion: int)-> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = "DELETE FROM tipo_habitacion WHERE id_habitacion=%s"
                cursor.execute(query, (id_habitacion,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar eliminar la habitacion.")
            raise e
        