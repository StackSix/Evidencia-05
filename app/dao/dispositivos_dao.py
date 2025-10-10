# src/app/dao/dispositivos_dao.py
from __future__ import annotations
from typing import Optional, List, Dict, Any
from app.conn.cursor import get_cursor

class DispositivoDAO:
    #CREATE -----------------
    @staticmethod
    def crear_dispositivo(
            id_dispositivo: str,
            id_habitacion: int,
            estado_dispositivo: bool,
            accion: str) -> int:
        if id_dispositivo is None:
            query = """
                INSERT INTO dispositivos (id_dispositivo, id_habitacion, estado_dispositivo, accion)
                VALUES (%s, %s, %s, %s)
            """
            params = (id_dispositivo, id_habitacion, estado_dispositivo, accion)
        else:
            query = """
                INSERT INTO dispositivos (id, tipo, estado_dispositivo, usuario_id)
                VALUES (%s, %s, %s, %s)
            """
            params = (id, tipo, estado_dispositivo, usuario_id)

        with get_cursor(commit=True) as cur:
            cur.execute(query, params)
            return cur.lastrowid or id

    @staticmethod
    def crear_camara(dispositivo_id: int,
                     nombre: str,
                     modelo: str,
                     grabacion_modo: str = "AUTO",
                     estado_automatizacion: bool = False) -> None:
        """
        Inserta la fila correspondiente en tabla `camara`. Asume que el
        dispositivo ya existe en `dispositivos`.
        """
        query = """
            INSERT INTO camara (dispositivo_id, nombre, modelo, grabacion_modo, estado_automatizacion)
            VALUES (%s, %s, %s, %s, %s)
        """
        with get_cursor(commit=True) as cur:
            cur.execute(query, (dispositivo_id, nombre, modelo, grabacion_modo, estado_automatizacion))

    # ----------------- READ -----------------
    @staticmethod
    def obtener_por_id(device_id: int) -> Optional[Dict[str, Any]]:
        query = "SELECT id, tipo, estado_dispositivo, usuario_id FROM dispositivos WHERE id = %s"
        with get_cursor() as cur:
            cur.execute(query, (device_id,))
            return cur.fetchone()

    @staticmethod
    def listar_todos() -> List[Dict[str, Any]]:
        query = "SELECT id, tipo, estado_dispositivo, usuario_id FROM dispositivos ORDER BY id"
        with get_cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    @staticmethod
    def listar_por_usuario(usuario_id: int) -> List[Dict[str, Any]]:
        query = "SELECT id, tipo, estado_dispositivo FROM dispositivos WHERE usuario_id = %s ORDER BY id"
        with get_cursor() as cur:
            cur.execute(query, (usuario_id,))
            return cur.fetchall()

    @staticmethod
    def obtener_camara_por_dispositivo_id(dispositivo_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT c.dispositivo_id, c.nombre, c.modelo, c.grabacion_modo, c.estado_automatizacion,
                   d.tipo, d.estado_dispositivo, d.usuario_id
            FROM camara c
            JOIN dispositivos d ON d.id = c.dispositivo_id
            WHERE c.dispositivo_id = %s
        """
        with get_cursor() as cur:
            cur.execute(query, (dispositivo_id,))
            return cur.fetchone()

    @staticmethod
    def listar_camaras_por_usuario(usuario_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT c.dispositivo_id AS id, c.nombre, c.modelo, c.grabacion_modo, c.estado_automatizacion,
                   d.estado_dispositivo
            FROM camara c
            JOIN dispositivos d ON d.id = c.dispositivo_id
            WHERE d.usuario_id = %s
            ORDER BY c.dispositivo_id
        """
        with get_cursor() as cur:
            cur.execute(query, (usuario_id,))
            return cur.fetchall()

    # ----------------- UPDATE -----------------
    @staticmethod
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

    # ----------------- DELETE -----------------
    @staticmethod
    def eliminar(device_id: int) -> None:
        """
        Eliminar dispositivo. Dado que `camara` tiene FK ON DELETE CASCADE a dispositivos
        (según DDL), bastará con borrar de `dispositivos`.
        """
        query = "DELETE FROM dispositivos WHERE id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (device_id,))

    @staticmethod
    def eliminar_camara(dispositivo_id: int) -> None:
        """
        Si por algún motivo querés borrar solo la fila de camara (y conservar el dispositivo),
        usalo. En general, preferible borrar desde `eliminar`.
        """
        query = "DELETE FROM camara WHERE dispositivo_id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (dispositivo_id,))
