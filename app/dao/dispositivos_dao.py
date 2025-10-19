from __future__ import annotations
from typing import Optional, List, Dict, Any
import mysql.connector
from app.conn.cursor import get_cursor
from app.conn.logger import logger
from app.dominio.dispositivos import Dispositivo
from app.dao.interfaces.i_dispositivo_dao import IDispositivoDAO

class DispositivoDAO(IDispositivoDAO):
    @staticmethod
    def registrar_dispositivo(id_domicilio: Optional[int], id_tipo: int, etiqueta: str) -> int:
        try:
            with get_cursor(commit=True) as cursor:
                query = """INSERT INTO dispositivos (id_domicilio, id_tipo, estado, etiqueta)
                    VALUES (%s, %s, TRUE, %s)"""
                cursor.execute(query, (id_domicilio, id_tipo, etiqueta))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("No se pudo registrar el dispositivo en la Base de Datos.")
            raise e
    
    @staticmethod #Esto configurarlo para usuario comun
    def obtener_dispositivo_usuario(id_usuario: int) -> List[Dispositivo]:
        try:
            with get_cursor(dictionary=True) as cursor:
                query = """
                    Implementar nueva query
                """
        
                cursor.execute(query, (id_usuario,))
                rows = cursor.fetchall()
            dispositivos = []
            for row in rows:
                dispositivos.append(
                    Dispositivo(
                        id_dispositivo=row["id_dispositivo"], 
                        id_domicilio=row["id_domicilio"],
                        id_tipo=row["id_tipo"], 
                        estado=row["estado"], 
                        etiqueta=row["etiqueta"]
                        )
                    )
            return dispositivos
        except mysql.connector.Error as e:
            logger.exception("No se pudieron obtener los dispositivos registrados.")
            raise e
    
    @staticmethod #Esto configurarlo para admin
    def obtener_todos_dispositivos() -> List[Dispositivo]:
        try:
            with get_cursor(dictionary=True) as cursor:
                query = """
                    Implementar
                """
                cursor.execute(query)
                rows = cursor.fetchall()
            dispositivos = []
            for row in rows:
                dispositivos.append(
                    Dispositivo(
                        id_dispositivo=row["id_dispositivo"], 
                        id_domicilio=row["id_domicilio"],
                        id_tipo=row["id_tipo"], 
                        estado=row["estado"], 
                        etiqueta=row["etiqueta"]
                        )
                    )
            return dispositivos
        except mysql.connector.Error as e:
            logger.exception("No se pudieron obtener los dispositivos registrados.")
            raise e

    @staticmethod 
    def actualizar_dispositivo(id_dispositivo: int, *,
                   id_domicilio: Optional[int] = None,
                   id_tipo: Optional[int] = None,
                   etiqueta: Optional[str] = None) -> None:
        sets, params = [], []
        if id_domicilio is not None: sets.append("id_habitacion=%s"); params.append(id_domicilio)
        if id_tipo is not None:      sets.append("id_tipo=%s");       params.append(id_tipo)
        if etiqueta:                 sets.append("etiqueta=%s");      params.append(etiqueta)
        if not sets: return
        params.append(id_dispositivo)
        sql = f"UPDATE dispositivos SET {', '.join(sets)} WHERE id_dispositivo=%s"
        with get_cursor(commit=True) as cur:
            cur.execute(sql, tuple(params))

    @staticmethod
    def eliminar_dispositivo(id_dispositivo: int) -> None:
        with get_cursor(commit=True) as cur:
            cur.execute("DELETE FROM dispositivos WHERE id_dispositivo=%s", (id_dispositivo,))
            
    @staticmethod #Esto si se logra con una funcion de arriba, eliminar
    def listar_dispositivos_por_domicilio(id_hogar: int) -> list[Dispositivo]:
        """
        Devuelve todos los dispositivos de todas las habitaciones de un hogar.
        """
        with get_cursor(dictionary=True) as cursor:
            query = """
                SELECT d.id_dispositivo, d.id_habitacion, d.id_tipo, d.estado, d.etiqueta
                FROM dispositivos d
                JOIN tipo_habitacion th ON d.id_habitacion = th.id_habitacion
                WHERE th.hogar_id = %s
            """
            cursor.execute(query, (id_hogar,))
            rows = cursor.fetchall()

        dispositivos = []
        for row in rows:
            dispositivos.append(
                Dispositivo(
                    id_dispositivo=row["id_dispositivo"],
                    id_tipo=row["id_tipo"],
                    estado=row["estado"],
                    etiqueta=row["etiqueta"]
                )
            )
        return dispositivos
    