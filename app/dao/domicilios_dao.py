# src/app/dao/domicilios_dao.py
from typing import List, Dict
from app.conn.cursor import get_cursor

class DomiciliosDAO:
    @staticmethod
    def crear(direccion: str, numeracion: str, ciudad: str, nombre_domicilio: str) -> int:
        q = """INSERT INTO domicilios (direccion, numeracion, ciudad, nombre_domicilio)
               VALUES (%s, %s, %s, %s)"""
        with get_cursor(commit=True) as cur:
            cur.execute(q, (direccion, numeracion, ciudad, nombre_domicilio))
            return cur.lastrowid

    @staticmethod
    def vincular_usuario(user_id: int, hogar_id: int) -> None:
        q = "INSERT IGNORE INTO usuarios_domicilios (usuario_id, hogar_id) VALUES (%s, %s)"
        with get_cursor(commit=True) as cur:
            cur.execute(q, (user_id, hogar_id))

    @staticmethod
    def obtener_por_usuario(user_id: int) -> List[Dict]:
        q = """
        SELECT h.id_hogar, h.nombre_domicilio, h.direccion, h.ciudad
        FROM usuarios_domicilios uh
        JOIN domicilios h ON h.id_hogar = uh.hogar_id
        WHERE uh.usuario_id = %s
        ORDER BY h.id_hogar
        """
        with get_cursor() as cur:
            cur.execute(q, (user_id,))
            return cur.fetchall()
