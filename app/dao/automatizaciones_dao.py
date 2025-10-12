from __future__ import annotations
from typing import Optional
import mysql.connector
from mysql.connector import Error
from interfaz_dao import DataAccessDAO 
from app.dominio.automatizacion import Automatizacion
from app.conn.cursor import get_cursor
from app.conn.logger import logger

class AutomatizacionesDAO(DataAccessDAO):
    def crear(self, automatizacion: Automatizacion)-> None:
        "Para insertar un registro en una tabla."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO automatizaciones (id_hogar, nombre, accion, dispositivo_asociado, estado, hora_encendido, hora_apagado) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (automatizacion.id_hogar, automatizacion.nombre, automatizacion.accion, automatizacion.dispositivo_asociado, automatizacion.estado, automatizacion.hora_encendido, automatizacion.hora_apagado))
                return cursor.lastrowid #ID generado por autoincremental
        except mysql.connector.Error:
            logger.exception("No se ha podido registrar la automatización.")
            raise
    
    def leer(self, automatizacion_id: int)-> Optional[Automatizacion]:
        "Recupera una automatización por su ID"
        try:
            with get_cursor(commit=False) as cursor:
                query = """
                    SELECT id_automatizacion, id_hogar, nombre, accion, dispositivo_asociado, estado, hora_encendido, hora_apagado
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
                        row["accion"],
                        row["dispositivo_asociado"],
                        row["estado"],
                        row["hora_encendido"],
                        row["hora_apagado"]
                        )
                return None
        except mysql.connector.Error as err:
            logger.exception("Error al intentar recuperar la Automatización por ID.")
            raise
    """          
    def get_all(self)-> list:
        "Recupera todos los registros de Automatizaciones."
        automatizaciones = []
        try:
            with get_cursor() as cursor:
                query = 
                    SELECT id_automatizacion, id_hogar, nombre, accion
                    FROM automatizaciones
                
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
    """
    def actualizar(self, automatizacion: Automatizacion)-> None:
        "Permite actualizar un registro de una automatización en la BD."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                UPDATE automatizaciones 
                SET id_hogar=%s, nombre=%s, accion=%s, dispositivo_asociado=%s, estado=%s, hora_encendido=%s, hora_apagado=%s
                WHERE id_automatizacion=%s
                """
                cursor.execute(query, (automatizacion.id_hogar, automatizacion.nombre, automatizacion.accion, automatizacion.dispositivo_asociado, automatizacion.estado, automatizacion.hora_encendido, automatizacion.hora_apagado))
        except mysql.connector.Error:
            logger.exception(f"Error al actualizar la automatización con ID: {automatizacion.id_automatizacion}")
            raise
            
    def eliminar(self, automatizacion: Automatizacion)-> None:
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
        