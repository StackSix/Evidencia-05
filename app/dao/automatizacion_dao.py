from __future__ import annotations
from typing import Optional, List
import mysql.connector
from app.dominio.automatizacion import Automatizacion
from app.conn.cursor import get_cursor
from app.conn.logger import logger
from app.dao.interfaces.i_automatizacion_dao import IAutomatizacionDAO

class AutomatizacionDAO(IAutomatizacionDAO):
    @staticmethod
    def registrar_automatizacion(automatizacion: Automatizacion) -> int:
        "Inserta un registro en la tabla y devuelve un ID asignado."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO automatizacion (id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (automatizacion.id_domicilio, automatizacion.nombre, automatizacion.accion, automatizacion.estado, automatizacion.hora_encendido, automatizacion.hora_apagado))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("No se ha podido registrar la automatización.")
            raise e
    
    @staticmethod
    def obtener_automatizacion(id_automatizacion: int) -> Optional[Automatizacion]:
        "Recupera una automatización por su ID."
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT id_automatizacion, id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado
                    FROM automatizacion
                    WHERE id_automatizacion = %s
                """
                cursor.execute(query, (id_automatizacion,))
                row = cursor.fetchone()
                if row:
                    return Automatizacion(
                        id_automatizacion=row["id_automatizacion"], 
                        id_domicilio=row["id_domicilio"], 
                        nombre=row["nombre"], 
                        accion=row["accion"],
                        estado=bool(row["estado"]),
                        hora_encendido=row["hora_encendido"],
                        hora_apagado=row["hora_apagado"]
                    )
        except mysql.connector.Error as e:
            logger.exception("Error al intentar recuperar la Automatización por ID.")
            raise e

    @staticmethod 
    def obtener_todas() -> List[Automatizacion]:
        "Recupera todas las automatizaciones."
        try:
            with get_cursor(dictionary=True) as cursor:
                query = """
                    SELECT id_automatizacion, id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado
                    FROM automatizacion
                    ORDER BY id_automatizacion
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                automatizaciones: List[Automatizacion] = []
                for row in rows:
                    automatizaciones.append(
                        Automatizacion(
                            id_automatizacion=row["id_automatizacion"], 
                            id_domicilio=row["id_domicilio"],
                            nombre=row["nombre"],
                            accion=row["accion"],
                            estado=bool(row["estado"]),
                            hora_encendido=row["hora_encendido"],
                            hora_apagado=row["hora_apagado"]
                        )
                    )
                return automatizaciones
        except mysql.connector.Error as err:
            logger.exception("Error al recuperar automatizaciones activas.")
            return []    
        
    @staticmethod
    def obtener_automatizaciones_por_domicilio(id_domicilio: int) -> list[Automatizacion]:
        """
        Devuelve todas las automatizaciones asociadas a un domicilio específico.
        """
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT id_automatizacion, id_domicilio, nombre, accion, estado, hora_encendido, hora_apagado
                    FROM automatizacion
                    WHERE id_domicilio = %s
                """
                cursor.execute(query, (id_domicilio,))
                rows = cursor.fetchall()
                
                automatizaciones = []
                for row in rows:
                    automatizaciones.append(
                        Automatizacion(
                            id_automatizacion=row["id_automatizacion"],
                            id_domicilio=row["id_domicilio"],
                            nombre=row["nombre"],
                            accion=row["accion"],
                            estado=bool(row["estado"]),
                            hora_encendido=row["hora_encendido"],
                            hora_apagado=row["hora_apagado"]
                        )
                    )
                return automatizaciones
        except mysql.connector.Error as e:
            logger.exception("Error al obtener automatizaciones por domicilio.")
            raise e

    @staticmethod
    def actualizar_automatizacion(automatizacion: Automatizacion) -> bool:
        "Permite actualizar un registro de una automatización en la BD."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE automatizacion
                    SET id_domicilio=%s, nombre=%s, accion=%s, estado=%s, hora_encendido=%s, hora_apagado=%s
                    WHERE id_automatizacion=%s
                """
                cursor.execute(query, (automatizacion.id_domicilio, automatizacion.nombre, automatizacion.accion, 1 if automatizacion.estado else 0, automatizacion.hora_encendido, automatizacion.hora_apagado, automatizacion.id_automatizacion))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception(f"Error al actualizar la automatización con ID: {automatizacion.id_automatizacion}")
            raise e
            
    @staticmethod
    def eliminar_automatizacion(id_automatizacion: int) -> bool:
        "Permite eliminar el registro de una automatización de la BD por su ID."
        try:
            with get_cursor(commit=True) as cursor:
                query = "DELETE FROM automatizacion WHERE id_automatizacion = %s"
                cursor.execute(query, (id_automatizacion,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception(f"Error al intentar eliminar la automatización con ID: {id_automatizacion}")
            raise e
        