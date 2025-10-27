from __future__ import annotations
import mysql.connector
from typing import List, Optional
from conn.cursor import get_cursor
from dao.interfaces.i_domicilio_dao import IDomicilioDAO
from dominio.domicilio import Domicilio
from conn.logger import logger

class DomicilioDAO(IDomicilioDAO):
    @staticmethod
    def registrar_domicilio(direccion: str, ciudad: str, nombre_domicilio: str, id_usuario: int) -> int:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO domicilio (direccion, ciudad, nombre_domicilio, id_usuario)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (direccion, ciudad, nombre_domicilio, id_usuario))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("Error al intentar registrar domicilio.")
            raise e
            
    @staticmethod
    def obtener_domicilio_usuario(id_usuario: int) -> Optional[List[Domicilio]]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT id_domicilio, nombre_domicilio, direccion, ciudad
                    FROM domicilio
                    WHERE id_usuario = %s
                    ORDER BY id_domicilio
                """
                cursor.execute(query, (id_usuario,))
                rows = cursor.fetchall()
            domicilios: List[Domicilio] = []
            for row in rows:
                domicilios.append(
                    Domicilio(
                        id_domicilio=row["id_domicilio"],
                        direccion=row["direccion"],
                        ciudad=row["ciudad"],
                        nombre_domicilio=row["nombre_domicilio"]
                )
            )
            return domicilios
        except mysql.connector.Error as e:
            logger.exception("Error al intentar recuperar los datos del usuario y su domicilio.")
            raise e
        
    @staticmethod
    def obtener_todos_domicilios() -> List[Domicilio]:
        try:
            with get_cursor(dictionary=True) as cursor:
                query = """
                    SELECT id_domicilio, direccion, ciudad, nombre_domicilio, id_usuario
                    FROM domicilio
                    ORDER BY id_domicilio
                """
                cursor.execute(query)
                rows = cursor.fetchall()
            domicilios: List[Domicilio] = []
            for row in rows:
                domicilios.append(
                    Domicilio(
                        id_domicilio=row["id_domicilio"],
                        direccion=row["direccion"],
                        ciudad=row["ciudad"],
                        nombre_domicilio=row["nombre_domicilio"]
                    )
                )
            return domicilios
        except mysql.connector.Error as e:
            logger.exception("Error al intentar obtener domicilios.")
            raise e
    
    @staticmethod
    def actualizar_domicilio(id_domicilio: int, direccion: str, ciudad: str, nombre_domicilio: str) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE domicilio
                    SET direccion=%s, ciudad=%s, nombre_domicilio=%s
                    WHERE id_domicilio=%s
                """
                cursor.execute(query, (direccion, ciudad, nombre_domicilio, id_domicilio))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar modificar datos del domicilio.")
            raise e
        
    @staticmethod
    def eliminar_domicilio(id_domicilio: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = "DELETE FROM domicilio WHERE id_domicilio=%s"
                cursor.execute(query, (id_domicilio,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar eliminar el domicilio.")
            raise e
        