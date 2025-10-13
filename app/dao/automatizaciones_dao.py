from __future__ import annotations
from typing import Optional, List
import mysql.connector
from mysql.connector import Error
from app.dao.interfaz_dao import DataAccessDAO 
from app.dominio.automatizacion import Automatizacion
from app.conn.cursor import get_cursor
from app.conn.logger import logger

class AutomatizacionesDAO(DataAccessDAO):
    @staticmethod
    def crear(automatizacion: Automatizacion) -> int:
        "Inserta un registro en la tabla y devuelve un ID asignado."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO automatizaciones (id_hogar, nombre, accion)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (automatizacion.id_hogar, automatizacion.nombre, automatizacion.accion))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("No se ha podido registrar la automatización.")
            raise e
    
    @staticmethod
    def leer(automatizacion_id: int) -> Optional[Automatizacion]:
        "Recupera una automatización por su ID."
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT id_automatizacion, id_hogar, nombre, accion
                    FROM automatizaciones
                    WHERE id_automatizacion=%s
                """
                cursor.execute(query, (automatizacion_id,))
                row = cursor.fetchone()
                if row:
                    return Automatizacion(
                        id_automatizacion=row["id_automatizacion"], 
                        id_hogar=row["id_hogar"], 
                        nombre=row["nombre"], 
                        accion=row["accion"]
                    )
                return None
        except mysql.connector.Error as e:
            logger.exception("Error al intentar recuperar la Automatización por ID.")
            raise e

    @staticmethod
    def leer_todas() -> list[dict]:
        "Recupera todas las automatizaciones sin filtrar por estado."
        try:
            with get_cursor(dictionary=True) as cursor:
                query = "SELECT id_automatizacion, id_hogar, nombre, accion FROM automatizaciones"
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            logger.exception("Error al recuperar automatizaciones.")
            return []

    @staticmethod
    def listar_domicilios_del_usuario(dni: str) -> list[dict]:
        """
        Retorna los domicilios asociados a un usuario según la tabla usuarios_hogares.
        """
        try:
            with get_cursor(dictionary=True) as cursor:
                query = """
                SELECT h.id_hogar, h.nombre_domicilio, h.direccion
                FROM domicilios h
                INNER JOIN usuarios_hogares uh ON h.id_hogar = uh.hogar_id
                INNER JOIN usuarios u ON uh.usuario_id = u.id
                WHERE u.dni = %s
                """
                cursor.execute(query, (dni,))
                return cursor.fetchall()
        except Exception as e:
            logger.exception("Error al listar domicilios del usuario.")
            return []
    
    @staticmethod
    def actualizar(automatizacion: Automatizacion) -> bool:
        "Permite actualizar un registro de una automatización en la BD."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                UPDATE automatizaciones 
                SET id_hogar=%s, nombre=%s, accion=%s
                WHERE id_automatizacion=%s
                """
                cursor.execute(query, (automatizacion.id_hogar, automatizacion.nombre, automatizacion.accion, automatizacion.id_automatizacion))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception(f"Error al actualizar la automatización con ID: {automatizacion.id_automatizacion}")
            raise e
            
    @staticmethod
    def eliminar(id_automatizacion: int) -> bool:
        "Permite eliminar el registro de una automatización de la BD por su ID."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                DELETE FROM automatizaciones 
                WHERE id_automatizacion=%s
                """
                cursor.execute(query, (id_automatizacion,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception(f"Error al intentar eliminar la automatización con ID: {id_automatizacion}")
            raise e
    
    @staticmethod
    def es_dueno_de_hogar(usuario_id: int, hogar_id: int) -> bool:
        """
        Verifica si un usuario es el propietario de un hogar.
        Utiliza una tabla intermedia 'usuarios_domicilios' para la validación.
        """
        try:
            with get_cursor(commit=False) as cursor:
                query = """
                    SELECT COUNT(ud.usuario_id)
                    FROM usuarios_hogares AS ud
                    WHERE ud.hogar_id = %s AND usuario_id = %s
                """
                cursor.execute(query, (hogar_id, usuario_id))
                resultado = cursor.fetchone()
                return resultado[0] > 0 if resultado else False
        except mysql.connector.Error as e:
            logger.exception("Error al verificar la propiedad del hogar.")
            raise e
            
    @staticmethod
    def es_dueno_de_automatizacion(usuario_id: int, automatizacion_id: int) -> bool:
        """
        Verifica si un usuario es el propietario de la automatización.
        Utiliza la tabla intermedia 'usuarios_hogares' para la validación.
        """
        try:
            with get_cursor(commit=False) as cursor:
                query = """
                    SELECT COUNT(a.id_automatizacion)
                    FROM automatizaciones AS a
                    JOIN usuarios_hogares AS ud ON a.id_hogar = ud.hogar_id
                    WHERE a.id_automatizacion = %s AND ud.usuario_id = %s
                """
                cursor.execute(query, (automatizacion_id, usuario_id))
                resultado = cursor.fetchone()
                return resultado[0] > 0 if resultado else False
        except mysql.connector.Error as e:
            logger.exception("Error al verificar la propiedad de la automatización.")
            raise e
        