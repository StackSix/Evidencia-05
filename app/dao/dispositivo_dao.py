from __future__ import annotations
from typing import Optional, List
import mysql.connector
from app.conn.cursor import get_cursor
from app.conn.logger import logger
from app.dominio.dispositivo import Dispositivo
from app.dao.interfaces.i_dispositivo_dao import IDispositivoDAO

class DispositivoDAO(IDispositivoDAO):
    @staticmethod
    def registrar_dispositivo(id_domicilio: int, id_tipo: int, estado: str, etiqueta: str) -> int:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO dispositivo (id_domicilio, id_tipo, estado, etiqueta)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (id_domicilio, id_tipo, estado, etiqueta))
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("No se pudo registrar el dispositivo en la Base de Datos.")
            raise e
    
    @staticmethod 
    def obtener_dispositivo_usuario(id_usuario: int) -> List[Dispositivo]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT d.id_dispositivo, d.id_domicilio, d.id_tipo, d.estado, d.etiqueta
                    FROM dispositivo d
                    JOIN domicilio h ON d.id_domicilio = h.id_domicilio
                    JOIN usuario u ON h.id_usuario = u.id_usuario
                    WHERE u.id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                rows = cursor.fetchall()
            dispositivos: List[Dispositivo] = []
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
    def obtener_todos_dispositivos() -> List[Dispositivo]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT id_dispositivo, id_domicilio, id_tipo, estado, etiqueta
                    FROM dispositivo
                    ORDER BY id_dispositivo
                """
                cursor.execute(query)
                rows = cursor.fetchall()
            dispositivos: List[Dispositivo] = []
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
                   estado: Optional[str] = None,
                   etiqueta: Optional[str] = None) -> bool:
        sets, params = [], []
        if id_domicilio is not None: sets.append("id_domicilio=%s"); params.append(id_domicilio)
        if id_tipo is not None:      sets.append("id_tipo=%s");       params.append(id_tipo)
        if estado is not None:      sets.append("estado=%s");       params.append(estado)
        if etiqueta is not None: sets.append("etiqueta=%s"); params.append(etiqueta)
        if not sets: return False
        params.append(id_dispositivo)
        
        try:
            with get_cursor(commit=True) as cur:
                query = f"UPDATE dispositivo SET {', '.join(sets)} WHERE id_dispositivo=%s"
                cur.execute(query, tuple(params))
                return cur.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al actualizar dispositivo.")
            raise e


    @staticmethod
    def eliminar_dispositivo(id_dispositivo: int) -> bool:
        try:
            with get_cursor(commit=True) as cur:
                query = "DELETE FROM dispositivo WHERE id_dispositivo=%s"
                cur.execute(query, (id_dispositivo,))
                return cur.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al eliminar dispositivo.")
            raise e
            
    @staticmethod 
    def listar_dispositivos_por_domicilio(id_domicilio: int) -> list[Dispositivo]:
        """
        Devuelve todos los dispositivos de todas las habitaciones de un hogar.
        """
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT id_dispositivo, id_domicilio, id_tipo, estado, etiqueta
                    FROM dispositivo
                    WHERE id_domicilio = %s
                    ORDER BY id_dispositivo
                """
                cursor.execute(query, (id_domicilio,))
                rows = cursor.fetchall()
            dispositivos: List[Dispositivo] = []
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
            logger.exception("Error al listar dispositivos por domicilio.")
            raise e
        