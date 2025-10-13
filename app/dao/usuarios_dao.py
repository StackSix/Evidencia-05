# app/dao/usuarios_dao.py
"""Operaciones de acceso a datos para la tabla `usuarios` y entidades relacionadas."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import bcrypt
import mysql.connector

from app.conn.cursor import get_cursor
from app.conn.logger import logger


class UsuarioDAO:
    """Capa de acceso a datos para usuarios utilizando MySQL en la nube."""

    # ---------- CREATE ----------
    @staticmethod
    def crear_usuario(
        dni: int,
        id_rol: int,
        nombre: str,
        apellido: str,
        email: str,
        contrasena: str,
    ) -> int:
        """Inserta un usuario y devuelve el identificador generado."""
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = """
            INSERT INTO usuarios (dni, id_rol, nombre, apellido, email, contrasena_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (dni, id_rol, nombre, apellido, email, hashed))
                return cursor.lastrowid
        except mysql.connector.Error as exc:  # pragma: no cover
            logger.exception("No se pudo registrar el usuario en la base de datos.")
            raise exc

    # ---------- READ ----------
    @staticmethod
    def obtener_por_email(email: str) -> Optional[Dict[str, Any]]:
        query = """
            SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email,
                u.contrasena_hash AS contrasena,
                r.nombre AS rol        -- <== alias exactamente 'rol'
            FROM usuarios u
            LEFT JOIN rol r ON r.id_rol = u.id_rol
            WHERE u.email = %s
            LIMIT 1
        """
        try:
            # usa dictionary=True para obtener dicts
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except mysql.connector.Error as exc:
            logger.exception("Error al buscar el usuario por email.")
            raise exc

    @staticmethod
    def obtener_por_dni(dni: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email,
                u.contrasena_hash AS contrasena,
                r.nombre AS rol
            FROM usuarios u
            LEFT JOIN rol r ON r.id_rol = u.id_rol
            WHERE u.dni = %s
            LIMIT 1
        """
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query, (dni,))
                return cursor.fetchone()
        except mysql.connector.Error as exc:
            logger.exception("Error al buscar el usuario por DNI.")
            raise exc

    @staticmethod
    def obtener_todos() -> List[Dict[str, Any]]:
        query = """
            SELECT
                u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email,
                r.nombre AS rol_nombre
            FROM usuarios u
            LEFT JOIN rol r ON r.id_rol = u.id_rol
            ORDER BY u.id
        """
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except mysql.connector.Error as exc:  # pragma: no cover
            logger.exception("Error al listar los usuarios.")
            raise exc

    @staticmethod
    def obtener_id_rol_por_nombre(nombre_rol: str) -> Optional[int]:
        query = "SELECT id_rol FROM rol WHERE nombre = %s"
        try:
            with get_cursor(dictionary=True) as cursor:
                cursor.execute(query, (nombre_rol,))
                row = cursor.fetchone()
                return None if row is None else int(row["id_rol"])
        except mysql.connector.Error as exc:  # pragma: no cover
            logger.exception("Error al obtener el rol solicitado.")
            raise exc

    # ---------- UPDATE ----------
    @staticmethod
    def cambiar_rol(usuario_id: int, nuevo_id_rol: int) -> None:
        query = "UPDATE usuarios SET id_rol = %s WHERE id = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (nuevo_id_rol, usuario_id))
        except mysql.connector.Error as exc:  # pragma: no cover
            logger.exception("No se pudo actualizar el rol del usuario.")
            raise exc

    @staticmethod
    def actualizar_contrasena(dni: int, contrasena: str) -> None:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = "UPDATE usuarios SET contrasena_hash = %s WHERE dni = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (hashed, dni))
        except mysql.connector.Error as exc:  # pragma: no cover
            logger.exception("No se pudo actualizar la contraseña del usuario.")
            raise exc

    # ---------- DELETE ----------
    @staticmethod
    def eliminar(dni: int) -> None:
        query = "DELETE FROM usuarios WHERE dni = %s"
        try:
            with get_cursor(commit=True) as cursor:
                cursor.execute(query, (dni,))
        except mysql.connector.Error as exc:  # pragma: no cover
            logger.exception("No se pudo eliminar el usuario indicado.")
            raise exc
