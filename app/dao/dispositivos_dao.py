from __future__ import annotations
from typing import Optional, List, Dict, Any
import mysql.connector
from app.conn.cursor import get_cursor
from app.conn.logger import logger
from app.dominio.dispositivos import Dispositivo

class DispositivoDAO:
    @staticmethod
    def crear(id_habitacion: Optional[int], id_tipo: int, etiqueta: str) -> int:
        sql = """INSERT INTO dispositivos (id_habitacion, id_tipo, estado, etiqueta)
                 VALUES (%s, %s, FALSE, %s)"""
        with get_cursor(commit=True) as cur:
            cur.execute(sql, (id_habitacion, id_tipo, etiqueta))
            return cur.lastrowid

    @staticmethod
    def obtener_por_id(id_dispositivo: int) -> Optional[Dict[str, Any]]:
        sql = """SELECT d.id_dispositivo, d.id_habitacion, d.id_tipo, d.estado, d.etiqueta,
                        td.nombre_tipo, th.nombre_habitacion
                 FROM dispositivos d
                 LEFT JOIN tipos_dispositivos td ON td.id_tipo=d.id_tipo
                 LEFT JOIN tipo_habitacion th   ON th.id_habitacion=d.id_habitacion
                 WHERE d.id_dispositivo=%s"""
        with get_cursor(dictionary=True) as cur:
            cur.execute(sql, (id_dispositivo,))
            return cur.fetchone()
        
    @staticmethod
    def listar_todos() -> List[Dict[str, Any]]:
        sql = """SELECT d.id_dispositivo, d.etiqueta, d.estado,
                        td.nombre_tipo, th.nombre_habitacion, h.nombre_domicilio
                 FROM dispositivos d
                 LEFT JOIN tipos_dispositivos td ON td.id_tipo=d.id_tipo
                 LEFT JOIN tipo_habitacion th   ON th.id_habitacion=d.id_habitacion
                 LEFT JOIN domicilios h         ON h.id_hogar=th.hogar_id
                 ORDER BY d.id_dispositivo"""
        with get_cursor(dictionary=True) as cur:
            cur.execute(sql)
            return cur.fetchall()

    @staticmethod
    def listar_por_usuario(user_id: int) -> list[dict]:
        query = """
            SELECT d.id_dispositivo, d.etiqueta, d.estado,
                td.nombre_tipo, th.nombre_habitacion, h.nombre_domicilio
            FROM usuarios_hogares uh
            JOIN domicilios h ON h.id_hogar = uh.hogar_id
            LEFT JOIN tipo_habitacion th ON th.hogar_id = h.id_hogar
            LEFT JOIN dispositivos d ON d.id_habitacion = th.id_habitacion OR d.id_habitacion IS NULL
            LEFT JOIN tipos_dispositivos td ON td.id_tipo = d.id_tipo
            WHERE uh.usuario_id = %s
            ORDER BY d.id_dispositivo
        """
        with get_cursor(dictionary=True) as cur:
            cur.execute(query, (user_id,))
            return cur.fetchall()

    @staticmethod
    def actualizar(id_dispositivo: int, *,
                   id_habitacion: Optional[int] = None,
                   id_tipo: Optional[int] = None,
                   etiqueta: Optional[str] = None) -> None:
        sets, params = [], []
        if id_habitacion is not None: sets.append("id_habitacion=%s"); params.append(id_habitacion)
        if id_tipo is not None:       sets.append("id_tipo=%s");       params.append(id_tipo)
        if etiqueta:                  sets.append("etiqueta=%s");      params.append(etiqueta)
        if not sets: return
        params.append(id_dispositivo)
        sql = f"UPDATE dispositivos SET {', '.join(sets)} WHERE id_dispositivo=%s"
        with get_cursor(commit=True) as cur:
            cur.execute(sql, tuple(params))

    @staticmethod
    def set_estado(id_dispositivo: int, estado: bool) -> None:
        with get_cursor(commit=True) as cur:
            cur.execute("UPDATE dispositivos SET estado=%s WHERE id_dispositivo=%s",
                        (estado, id_dispositivo))

    @staticmethod
    def eliminar(id_dispositivo: int) -> None:
        with get_cursor(commit=True) as cur:
            cur.execute("DELETE FROM dispositivos WHERE id_dispositivo=%s", (id_dispositivo,))
            
    @staticmethod
    def listar_por_hogar(id_hogar: int) -> list[Dispositivo]:
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
                    id_habitacion=row["id_habitacion"],
                    id_tipo=row["id_tipo"],
                    estado=row["estado"],
                    etiqueta=row["etiqueta"]
                )
            )
        return dispositivos
    