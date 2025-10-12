from __future__ import annotations
from typing import Optional, List, Dict, Any
import mysql.connector
from mysql.connector import Error
from interfaz_dao import DataAccessDAO
from app.conn.cursor import get_cursor
from app.conn.logger import logger
from app.dominio.dispositivos import Dispositivo
from app.dominio.camaras import Camara

class DispositivoDAO(DataAccessDAO):
    @staticmethod
    def crear(
            id_habitacion: int,
            accion: str,
            estado: str,
            nombre_camara: str,
            grabacion_modo: str = "AUTO",
            estado_automatizacion: bool = False
    ) -> Camara | None:
        "Registra una nueva cámara en la base de datos y devuelve el objeto Camara."
        try:
            with get_cursor(commit=True) as cursor:
                # 1. Insertar en la tabla 'dispositivos'
                dispositivo_query = """
                    INSERT INTO dispositivos (id_habitacion, accion, estado)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(dispositivo_query, (id_habitacion, accion, estado))
                id_dispositivo = cursor.lastrowid
                
                if id_dispositivo:
                    camara_query = """
                        INSERT INTO camaras (dispositivo_id, nombre_camara, grabacion_modo, estado_automatizacion)
                        VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(camara_query, (id_dispositivo, nombre_camara, grabacion_modo, estado_automatizacion))

                    return Camara(
                        id_dispositivo=id_dispositivo,
                        id_habitacion=id_habitacion,
                        nombre_camara=nombre_camara,
                        grabacion_modo=grabacion_modo,
                        estado_automatizacion=estado_automatizacion,
                        accion=accion,
                        estado=estado
                    )
                else:
                    raise mysql.connector.Error("No se pudo obtener el ID del nuevo dispositivo.")
        except mysql.connector.Error as e:
            logger.exception("Error al intentar registrar la cámara y su dispositivo.")
            raise e

    @staticmethod
    def leer(id_dispositivo: int) -> Camara | None:
        try:
            with get_cursor(commit=False) as cursor:
                query = """
                    SELECT 
                        d.id_dispositivo, d.id_habitacion, d.accion, d.estado,
                        c.nombre_camara, c.grabacion_modo, c.estado_automatizacion
                    FROM dispositivos AS d
                    INNER JOIN camara AS c ON d.id_dispositivo = c.dispositivo_id
                    WHERE d.id_dispositivo = %s
                """
                cursor.execute(query, (id_dispositivo,))
                row = cursor.fetchone()

                if row:
                    return Camara(
                        row["id_dispositivo"], 
                        row["id_habitacion"], 
                        row["accion"], 
                        row["estado"],
                        row["nombre_camara"],
                        row["grabacion_modo"],
                        row["estado_automatizacion"]
                        )
                else:
                    return None  
        except mysql.connector.Error as e:
            logger.exception("Error al intentar leer la cámara.")
            raise e

    @staticmethod
    def actualizar(camara: Camara)-> bool:
        try:
            with get_cursor(commit=True) as cursor:
                dispositivo_query = """
                    UPDATE dispositivos
                    SET id_habitacion=%s 
                    WHERE id_dispositivo=%s 
                """
                cursor.execute(dispositivo_query, (camara.id_habitacion, camara.id_dispositivo))
                camara_query = """
                    UPDATE camaras
                    SET nombre_camara=%s, grabacion_modo=%s, estado_automatizacion=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(camara_query, (camara.nombre_camara, camara.grabacion_modo, camara.estado_automatizacion, camara.id_dispositivo))
                return cursor.rowcount > 0
        
        except mysql.connector.Error as e:
            logger.exception("Error al intentar modificar la camara.")
            raise e

    @staticmethod
    def eliminar(id_dispositivo: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:    
                camara_query = "DELETE FROM camaras WHERE id_dispositivo = %s"
                cursor.execute(camara_query, (id_dispositivo,))
                dispositivo_query = "DELETE FROM dispositivos WHERE id_dispositivo = %s"
                cursor.execute(dispositivo_query, (id_dispositivo,))
                return cursor.rowcount > 0
        
        except mysql.connector.Error as e:
            logger.exception("Error, no se pudo eliminar el dispositivo camara.")
            raise e

    @staticmethod
    def leer_por_dni_usuario(dni: int) -> List[Dict]:
        "Recupera dispositivos de un usuario a través de las tablas intermedias."
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT
                        d.id_dispositivo, d.accion, d.estado,
                        th.nombre_habitacion, dom.nombre_domicilio
                    FROM dispositivos d
                    JOIN tipo_habitacion th ON d.id_habitacion = th.id_habitacion
                    JOIN domicilios dom ON th.id_domicilio = dom.id_domicilio
                    WHERE dom.dni_propietario = %s
                """
                cursor.execute(query, (dni,))
                return cursor.fetchall()
        except mysql.connector.Error as e:
            logger.exception("Error al consultar dispositivos por DNI de usuario.")
            raise e
        