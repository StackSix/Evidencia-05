from __future__ import annotations
from typing import Optional, List
import mysql.connector
from mysql.connector import Error
from interfaz_dao import DataAccessDAO 
from app.dominio.automatizacion import Automatizacion
from app.conn.cursor import get_cursor
from app.conn.logger import logger

class AutomatizacionesDAO(DataAccessDAO):
    @staticmethod
    def crear(self, automatizacion: Automatizacion) -> int:
        "Inserta un registro en la tabla y devuelve un ID asignado."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO automatizaciones (id_hogar, nombre, accion, id_dispositivo_asociado, estado, hora_encendido, hora_apagado) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (automatizacion.id_hogar, automatizacion.nombre, automatizacion.accion, automatizacion.id_dispositivo_asociado, automatizacion.estado, automatizacion.hora_encendido, automatizacion.hora_apagado))
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
                    SELECT id_automatizacion, id_hogar, nombre, accion, id_dispositivo_asociado, estado, hora_encendido, hora_apagado
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
                        accion=row["accion"],
                        id_dispositivo_asociado=row["id_dispositivo_asociado"],
                        estado=row["estado"],
                        hora_encendido=row["hora_encendido"],
                        hora_apagado=row["hora_apagado"]
                    )
                return None
        except mysql.connector.Error as e:
            logger.exception("Error al intentar recuperar la Automatización por ID.")
            raise e

    @staticmethod
    def leer_todas_activas() -> List[Automatizacion]:
        "Recupera todas las automatizaciones que están activas."
        try:
            with get_cursor(dictionary=True) as cursor:
                query = "SELECT * FROM automatizaciones WHERE estado = 1"
                cursor.execute(query)
                rows = cursor.fetchall()
                automatizaciones = [
                    Automatizacion(
                        id_automatizacion=row["id_automatizacion"], 
                        id_hogar=row["id_hogar"],
                        nombre=row["nombre"],
                        accion=row["accion"],
                        id_dispositivo_asociado=row["id_dispositivo_asociado"],
                        estado=row["estado"],
                        hora_encendido=row["hora_encendido"],
                        hora_apagado=row["hora_apagado"]
                    ) for row in rows
                ]
                return automatizaciones
        except mysql.connector.Error as err:
            logger.exception("Error al recuperar automatizaciones activas.")
            return []    

    @staticmethod
    def actualizar(automatizacion: Automatizacion) -> bool:
        "Permite actualizar un registro de una automatización en la BD."
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                UPDATE automatizaciones 
                SET id_hogar=%s, nombre=%s, accion=%s, id_dispositivo_asociado=%s, estado=%s, hora_encendido=%s, hora_apagado=%s
                WHERE id_automatizacion=%s
                """
                cursor.execute(query, (automatizacion.id_hogar, automatizacion.nombre, automatizacion.accion, automatizacion.id_dispositivo_asociado, automatizacion.estado, automatizacion.hora_encendido, automatizacion.hora_apagado, automatizacion.id_automatizacion))
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
    def es_dueno_de_hogar(dni_usuario: int, id_hogar: int) -> bool:
        """
        Verifica si un usuario es el propietario de un hogar.
        Utiliza una tabla intermedia 'usuarios_domicilios' para la validación.
        """
        try:
            with get_cursor(commit=False) as cursor:
                query = """
                    SELECT COUNT(ud.dni)
                    FROM usuarios_domicilios AS ud
                    WHERE ud.id_domicilio = %s AND ud.dni = %s
                """
                cursor.execute(query, (id_hogar, dni_usuario))
                resultado = cursor.fetchone()
                # El resultado es una tupla, se comprueba el primer elemento
                return resultado[0] > 0 if resultado else False
        except mysql.connector.Error as e:
            logger.exception("Error al verificar la propiedad del hogar.")
            raise e
            
    @staticmethod
    def es_dueno_de_automatizacion(dni_usuario: int, automatizacion_id: int) -> bool:
        """
        Verifica si un usuario es el propietario de la automatización.
        Utiliza la tabla intermedia 'usuarios_domicilios' para la validación.
        """
        try:
            with get_cursor(commit=False) as cursor:
                query = """
                    SELECT COUNT(a.id_automatizacion)
                    FROM automatizaciones AS a
                    JOIN usuarios_domicilios AS ud ON a.id_hogar = ud.id_domicilio
                    WHERE a.id_automatizacion = %s AND ud.dni = %s
                """
                cursor.execute(query, (automatizacion_id, dni_usuario))
                resultado = cursor.fetchone()
                # El resultado es una tupla, se comprueba el primer elemento
                return resultado[0] > 0 if resultado else False
        except mysql.connector.Error as e:
            logger.exception("Error al verificar la propiedad de la automatización.")
            raise e
        