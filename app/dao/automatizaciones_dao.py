from __future__ import annotations
from typing import Optional
import mysql.connector
from mysql.connector import Error
from interfaz_dao import DataAccessDAO 
from app.dominio.automatizacion import Automatizacion
from app.conn.cursor import get_cursor
from app.conn.logger import logger


class AutomatizacionesDAO(DataAccessDAO):
    def create(self, automatizacion: Automatizacion)-> None:
        "Para insertar un registro en una tabla."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO automatizaciones (id_automatizacion, id_hogar, nombre, accion) 
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (automatizacion.id_automatizacion, automatizacion.id_hogar, automatizacion.nombre, automatizacion.accion))
        except mysql.connector.Error as err:
            logger.exception("No se ha podido registrar la automatización.")
            raise
    
    def get(self, automatizacion_id: int)-> Optional[Automatizacion]:
        "Recupera una automatización por su ID"
        try:
            with get_cursor() as cursor:
                query = """
                    SELECT id_automatizacion, id_hogar, nombre, accion
                    FROM automatizaciones
                    WHERE id_automatizacion=%s
                """
                cursor.execute(query, (automatizacion_id,))
                row = cursor.fetchone()
                if row:
                    return Automatizacion(
                        row["id_automatizacion"], 
                        row["id_hogar"], 
                        row["nombre"], 
                        row["accion"]
                        )
                return None
        except mysql.connector.Error as err:
            logger.exception("Error al intentar recuperar la Automatización por ID.")
            raise
                
    def get_all(self)-> list:
        "Recupera todos los registros de Automatizaciones."
        automatizaciones = []
        try:
            with get_cursor() as cursor:
                query = """
                    SELECT id_automatizacion, id_hogar, nombre, accion
                    FROM automatizaciones
                """
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    automatizaciones.append(Automatizacion(
                        row["id_automatizacion"], 
                        row["id_hogar"], 
                        row["nombre"], 
                        row["accion"]
                        ))
                return automatizaciones
        except mysql.connector.Error as err:
            logger.exception("Error al intentar recuperar todas las Automatizaciones.", err)
            return []
    
    def update(self, automatizacion: Automatizacion)-> None:
        "Permite actualizar un registro de una automatización en la BD."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                UPDATE automatizaciones 
                SET id_hogar=%s, nombre=%s, accion=%s 
                WHERE id_automatizacion=%s
                """
                cursor.execute(query, (automatizacion.id_hogar, automatizacion.nombre, automatizacion.accion, automatizacion.id_automatizacion))
        except mysql.connector.Error:
            logger.exception(f"Error al actualizar la automatización con ID: {automatizacion.id_automatizacion}")
            raise
            
    def delete(self, automatizacion: Automatizacion)-> None:
        "Permite eliminar el registro de una automatización de la BD."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                DELETE FROM automatizaciones 
                WHERE id_automatizacion=%s
                """
                cursor.execute(query, (automatizacion.id_automatizacion,))
        except mysql.connector.Error:
            logger.exception(f"Error al intentar eliminar la automatización con ID: {automatizacion.id_automatizacion}")
            raise