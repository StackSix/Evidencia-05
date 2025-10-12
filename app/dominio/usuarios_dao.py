# app/dao/usuarios_dao.py
from __future__ import annotations

from typing import Optional, List, Dict
import bcrypt
import mysql.connector

from app.conn.cursor import get_cursor
from app.conn.logger import logger


class UsuarioDAO:
    """
    Data Access Object para la tabla `usuarios`.

    Esquema esperado:
      - id                INT UNSIGNED AUTO_INCREMENT PRIMARY KEY
      - dni               INT NOT NULL UNIQUE
      - id_rol            INT UNSIGNED NOT NULL  (FK -> rol.id_rol)
      - nombre            VARCHAR(120) NOT NULL
      - apellido          VARCHAR(120) NOT NULL
      - email             VARCHAR(120) NOT NULL UNIQUE
      - contrasena_hash   VARCHAR(255) NOT NULL
      - creado_en         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    """

    # ---------- CREATE ----------
    @staticmethod
    def crear(
        dni: int,
        id_rol: int,
        nombre: str,
        apellido: str,
        email: str,
        contrasena_plana: str,
    ) -> int:
        """
        Inserta un nuevo usuario y devuelve el id generado.
        """
        hashed = bcrypt.hashpw(
            contrasena_plana.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        query = """
            INSERT INTO usuarios (dni, id_rol, nombre, apellido, email, contrasena_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(query, (dni, id_rol, nombre, apellido, email, hashed))
                return cur.lastrowid
        except mysql.connector.Error as exc:
            logger.exception("Error creando usuario (dni=%s, email=%s).", dni, email)
            raise exc

    # ---------- READ ----------
    @staticmethod
    def obtener_por_id(user_id: int) -> Optional[Dict]:
        query = """
            SELECT
                id, dni, id_rol, nombre, apellido, email,
                contrasena_hash AS contrasena,
                creado_en
            FROM usuarios
            WHERE id = %s
        """
        try:
            with get_cursor(dictionary=True) as cur:
                cur.execute(query, (user_id,))
                return cur.fetchone()
        except mysql.connector.Error as exc:
            logger.exception("Error obteniendo usuario por id=%s.", user_id)
            raise exc

    @staticmethod
    def obtener_por_email(email: str) -> Optional[Dict]:
        """
        Devuelve un dict con los campos del usuario. Alias de contrasena_hash -> 'contrasena'
        para que la capa de servicios pueda verificar el hash sin acoplarse al nombre de columna.
        """
        query = """
            SELECT
                id, dni, id_rol, nombre, apellido, email,
                contrasena_hash AS contrasena,
                creado_en
            FROM usuarios
            WHERE email = %s
        """
        try:
            with get_cursor(dictionary=True) as cur:
                cur.execute(query, (email,))
                return cur.fetchone()
        except mysql.connector.Error as exc:
            logger.exception("Error al buscar usuario por email=%s.", email)
            raise exc

    @staticmethod
    def obtener_por_dni(dni: int) -> Optional[Dict]:
        query = """
            SELECT
                id, dni, id_rol, nombre, apellido, email,
                contrasena_hash AS contrasena,
                creado_en
            FROM usuarios
            WHERE dni = %s
        """
        try:
            with get_cursor(dictionary=True) as cur:
                cur.execute(query, (dni,))
                return cur.fetchone()
        except mysql.connector.Error as exc:
            logger.exception("Error al buscar usuario por dni=%s.", dni)
            raise exc

    @staticmethod
    def obtener_todos() -> List[Dict]:
        query = """
            SELECT
                id, dni, id_rol, nombre, apellido, email,
                creado_en
            FROM usuarios
            ORDER BY id
        """
        try:
            with get_cursor(dictionary=True) as cur:
                cur.execute(query)
                return cur.fetchall()
        except mysql.connector.Error as exc:
            logger.exception("Error listando usuarios.")
            raise exc

    # ---------- UPDATE ----------
    @staticmethod
    def cambiar_rol(user_id: int, nuevo_id_rol: int) -> None:
        """
        Cambia el id_rol del usuario. (El control de permisos/rol lo hace la capa de servicios.)
        """
        query = "UPDATE usuarios SET id_rol = %s WHERE id = %s"
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(query, (nuevo_id_rol, user_id))
        except mysql.connector.Error as exc:
            logger.exception("Error cambiando rol de usuario id=%s -> id_rol=%s.", user_id, nuevo_id_rol)
            raise exc

    @staticmethod
    def actualizar_contrasena_por_dni(dni: int, nueva_contra: str) -> None:
        """
        Actualiza la contraseña por DNI. Útil cuando se valida identidad por DNI + email.
        """
        hashed = bcrypt.hashpw(
            nueva_contra.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        query = "UPDATE usuarios SET contrasena_hash = %s WHERE dni = %s"
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(query, (hashed, dni))
        except mysql.connector.Error as exc:
            logger.exception("Error actualizando contraseña (dni=%s).", dni)
            raise exc

    @staticmethod
    def actualizar_contrasena_por_id(user_id: int, nueva_contra: str) -> None:
        hashed = bcrypt.hashpw(
            nueva_contra.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        query = "UPDATE usuarios SET contrasena_hash = %s WHERE id = %s"
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(query, (hashed, user_id))
        except mysql.connector.Error as exc:
            logger.exception("Error actualizando contraseña (id=%s).", user_id)
            raise exc

    @staticmethod
    def actualizar_datos_basicos(
        user_id: int,
        nombre: Optional[str] = None,
        apellido: Optional[str] = None,
        email: Optional[str] = None,
    ) -> None:
        """
        Actualiza nombre/apellido/email si se proveen.
        """
        sets: List[str] = []
        params: List = []

        if nombre:
            sets.append("nombre = %s")
            params.append(nombre)
        if apellido:
            sets.append("apellido = %s")
            params.append(apellido)
        if email:
            sets.append("email = %s")
            params.append(email)

        if not sets:
            return  # nada que actualizar

        params.append(user_id)
        query = f"UPDATE usuarios SET {', '.join(sets)} WHERE id = %s"
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(query, tuple(params))
        except mysql.connector.Error as exc:
            logger.exception("Error actualizando datos básicos del usuario id=%s.", user_id)
            raise exc

    # ---------- DELETE ----------
    @staticmethod
    def eliminar_por_id(user_id: int) -> None:
        query = "DELETE FROM usuarios WHERE id = %s"
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(query, (user_id,))
        except mysql.connector.Error as exc:
            logger.exception("Error eliminando usuario id=%s.", user_id)
            raise exc

    @staticmethod
    def eliminar_por_dni(dni: int) -> None:
        query = "DELETE FROM usuarios WHERE dni = %s"
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(query, (dni,))
        except mysql.connector.Error as exc:
            logger.exception("Error eliminando usuario dni=%s.", dni)
            raise exc

    # ---------- Helpers (existencia) ----------
    @staticmethod
    def existe_email(email: str) -> bool:
        query = "SELECT 1 FROM usuarios WHERE email = %s LIMIT 1"
        try:
            with get_cursor() as cur:
                cur.execute(query, (email,))
                return cur.fetchone() is not None
        except mysql.connector.Error as exc:
            logger.exception("Error verificando existencia de email=%s.", email)
            raise exc

    @staticmethod
    def existe_dni(dni: int) -> bool:
        query = "SELECT 1 FROM usuarios WHERE dni = %s LIMIT 1"
        try:
            with get_cursor() as cur:
                cur.execute(query, (dni,))
                return cur.fetchone() is not None
        except mysql.connector.Error as exc:
            logger.exception("Error verificando existencia de dni=%s.", dni)
            raise exc
