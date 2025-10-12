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
    #CREATE -----------------
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

    # ----------------- READ -----------------
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
    """
    @staticmethod
    def leer_todos() -> List[Camara]:
        "Devuelve una lista con todos los objetos Camara de la base de datos."
        camaras = []
        try:
            # Asegúrate de que get_cursor devuelva un cursor con dictionary=True
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = 
                    SELECT 
                        d.id_dispositivo, d.id_habitacion, d.accion, d.estado,
                        c.nombre_camara, c.grabacion_modo, c.estado_automatizacion
                    FROM dispositivos AS d
                    INNER JOIN camara AS c ON d.id_dispositivo = c.dispositivo_id
                
                cursor.execute(query)
                rows = cursor.fetchall()  

                for row in rows:
                    camara = Camara(
                        id_dispositivo=row["id_dispositivo"], 
                        id_habitacion=row["id_habitacion"], 
                        accion=row["accion"], 
                        estado=row["estado"],
                        nombre_camara=row["nombre_camara"],
                        grabacion_modo=row["grabacion_modo"],
                        estado_automatizacion=row["estado_automatizacion"]
                    )
                    camaras.append(camara)
        except mysql.connector.Error:
            logger.exception("Error al intentar leer todas las cámaras.")
            return []
        return camaras
    
    @staticmethod
    def obtener_camara_por_dispositivo_id(dispositivo_id: int) -> Optional[Dict[str, Any]]:
        query = 
            SELECT c.dispositivo_id, c.nombre, c.grabacion_modo, c.estado_automatizacion,
                   d.tipo, d.estado_dispositivo, d.usuario_id
            FROM camara c
            JOIN dispositivos d ON d.id = c.dispositivo_id
            WHERE c.dispositivo_id = %s
        
        with get_cursor() as cur:
            cur.execute(query, (dispositivo_id,))
            return cur.fetchone()

    @staticmethod
    def listar_camaras_por_usuario(usuario_id: int) -> List[Dict[str, Any]]:
        query = 
            SELECT c.dispositivo_id AS id, c.nombre, c.grabacion_modo, c.estado_automatizacion,
                   d.estado_dispositivo
            FROM camara c
            JOIN dispositivos d ON d.id = c.dispositivo_id
            WHERE d.usuario_id = %s
            ORDER BY c.dispositivo_id
        
        with get_cursor() as cur:
            cur.execute(query, (usuario_id,))
            return cur.fetchall()
    """
    # ----------------- UPDATE -----------------
    @staticmethod
    def actualizar(camara: Camara)-> bool:
        try:
            with get_cursor(commit=True) as cursor:
                dispositivo_query = """
                    UPDATE dispositivos
                    SET id_habitacion=%s, 
                    WHERE id_dispositivo=%s 
                """
                cursor.execute(dispositivo_query, (camara.id_habitacion,))
                camara_query = """
                    UPDATE camaras
                    SET nombre_camara=%s, c.grabacion_modo=%s, c.estado_automatizacion=%s
                    WHERE id_dispositivo=%s
                """
                cursor.execute(camara_query, (camara.nombre_camara, camara.grabacion_modo, camara.estado_automatizacion))
                return cursor.rowcount > 0
        
        except mysql.connector.Error as e:
            logger.exception("Error al intentar modificar la camara.")
            raise e
    """
    def actualizar_estado(device_id: int, nuevo_estado: str) -> None:
        query = "UPDATE dispositivos SET estado_dispositivo = %s WHERE id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (nuevo_estado, device_id))

    @staticmethod
    def reasignar_usuario(device_id: int, nuevo_usuario_id: int) -> None:
        query = "UPDATE dispositivos SET usuario_id = %s WHERE id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (nuevo_usuario_id, device_id))

    @staticmethod
    def actualizar_tipo(device_id: int, nuevo_tipo: str) -> None:
        query = "UPDATE dispositivos SET tipo = %s WHERE id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (nuevo_tipo, device_id))

    @staticmethod
    def actualizar_camara(dispositivo_id: int,
                          nombre: Optional[str] = None,
                          modelo: Optional[str] = None,
                          grabacion_modo: Optional[str] = None,
                          estado_automatizacion: Optional[bool] = None) -> None:
        # construimos query dinámico según campos no None
        campos = []
        params: List[Any] = []
        if nombre is not None:
            campos.append("nombre = %s"); params.append(nombre)
        if modelo is not None:
            campos.append("modelo = %s"); params.append(modelo)
        if grabacion_modo is not None:
            campos.append("grabacion_modo = %s"); params.append(grabacion_modo)
        if estado_automatizacion is not None:
            campos.append("estado_automatizacion = %s"); params.append(bool(estado_automatizacion))

        if not campos:
            return  # nada que actualizar

        sql = "UPDATE camara SET " + ", ".join(campos) + " WHERE dispositivo_id = %s"
        params.append(dispositivo_id)
        with get_cursor(commit=True) as cur:
            cur.execute(sql, tuple(params))
    """
    # ----------------- DELETE -----------------
    @staticmethod
    def eliminar(id_dispositivo: int) -> bool:
        """
        Eliminar dispositivo. Dado que `camara` tiene FK ON DELETE CASCADE a dispositivos
        (según DDL), bastará con borrar de `dispositivos`.
        """
        try:
            with get_cursor(commit=True) as cursor:    
                camara_query = "DELETE FROM camaras WHERE id_dispositivo = %s"
                cursor.execute(camara_query, (id_dispositivo))
                dispositivo_query = "DELETE FROM dispositivos WHERE id_dispositivo = %s"
                cursor.execute(dispositivo_query, (id_dispositivo))
                return cursor.rowcount > 0
        
        except mysql.connector.Error as e:
            logger.exception("Error, no se pudo eliminar el dispositivo camara.")
            raise e
    """    
    @staticmethod
    def eliminar_camara(dispositivo_id: int) -> None:
        
        Si por algún motivo querés borrar solo la fila de camara (y conservar el dispositivo),
        usalo. En general, preferible borrar desde `eliminar`.
        
        query = "DELETE FROM camara WHERE dispositivo_id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (dispositivo_id,))
    """