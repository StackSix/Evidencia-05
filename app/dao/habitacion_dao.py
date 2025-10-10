# src/app/dao/habitacion_dao.py
from typing import List, Dict
from app.conn.cursor import get_cursor

class HabitacionDAO:
    @staticmethod
    def crear(hogar_id: int, nombre_habitacion: str) -> int:
        q = "INSERT INTO tipo_habitacion (hogar_id, nombre_habitacion) VALUES (%s, %s)"
        with get_cursor(commit=True) as cur:
            cur.execute(q, (hogar_id, nombre_habitacion))
            return cur.lastrowid

    @staticmethod
    def obtener_por_hogar(hogar_id: int) -> List[Dict]:
        q = "SELECT id_habitacion, nombre_habitacion FROM tipo_habitacion WHERE hogar_id = %s ORDER BY id_habitacion"
        with get_cursor() as cur:
            cur.execute(q, (hogar_id,))
            return cur.fetchall()
