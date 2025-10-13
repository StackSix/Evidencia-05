# app/dao/usuarios_dao.py
from __future__ import annotations
from typing import Optional, List, Dict, Any
import bcrypt
import mysql.connector

from app.conn.cursor import get_cursor
from app.conn.logger import logger

class UsuarioDAO:
    # ---------- CREATE ----------
    @staticmethod
    def crear(dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena_plana: str) -> int:
        hashed = bcrypt.hashpw(contrasena_plana.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = """
            INSERT INTO usuarios (dni, id_rol, nombre, apellido, email, contrasena_hash)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with get_cursor(commit=True) as cur:
            cur.execute(query, (dni, id_rol, nombre, apellido, email, hashed))
            return cur.lastrowid

    # Alias para compatibilidad con AuthService
    @staticmethod
    def crear_usuario(dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena_plana: str) -> int:
        return UsuarioDAO.crear(dni, id_rol, nombre, apellido, email, contrasena_plana)

    # ---------- READ ----------
    @staticmethod
    def obtener_por_id(user_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email,
                   r.nombre AS rol_nombre
            FROM usuarios u
            LEFT JOIN rol r ON r.id_rol = u.id_rol
            WHERE u.id = %s
        """
        with get_cursor(dictionary=True) as cur:
            cur.execute(query, (user_id,))
            return cur.fetchone()

    @staticmethod
    def obtener_por_email(email: str) -> Optional[Dict]:
        query = """
            SELECT id, dni, id_rol, nombre, apellido, email,
                   contrasena_hash AS contrasena, creado_en
            FROM usuarios WHERE email = %s
        """
        with get_cursor(dictionary=True) as cur:
            cur.execute(query, (email,))
            return cur.fetchone()

    @staticmethod
    def obtener_por_dni(dni: int) -> Optional[Dict]:
        query = """
            SELECT id, dni, id_rol, nombre, apellido, email,
                   contrasena_hash AS contrasena, creado_en
            FROM usuarios WHERE dni = %s
        """
        with get_cursor(dictionary=True) as cur:
            cur.execute(query, (dni,))
            return cur.fetchone()

    @staticmethod
    def obtener_todos() -> List[Dict]:
        query = "SELECT id, dni, id_rol, nombre, apellido, email, creado_en FROM usuarios ORDER BY id"
        with get_cursor(dictionary=True) as cur:
            cur.execute(query)
            return cur.fetchall()

    # ---------- UPDATE ----------
    @staticmethod
    def cambiar_rol(user_id: int, nuevo_id_rol: int) -> None:
        with get_cursor(commit=True) as cur:
            cur.execute("UPDATE usuarios SET id_rol = %s WHERE id = %s", (nuevo_id_rol, user_id))

    @staticmethod
    def actualizar_contrasena_por_dni(dni: int, nueva_contra: str) -> None:
        import bcrypt, mysql.connector
        from app.conn.cursor import get_cursor
        from app.conn.logger import logger

        hashed = bcrypt.hashpw(nueva_contra.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = "UPDATE usuarios SET contrasena_hash = %s WHERE dni = %s"
        try:
            with get_cursor(commit=True) as cur:
                cur.execute(query, (hashed, dni))
        except mysql.connector.Error as exc:
            logger.exception("Error actualizando contraseña (dni=%s).", dni)
            raise exc
        
    @staticmethod
    def actualizar_contrasena_por_id(user_id: int, nueva_contra: str) -> None:
        hashed = bcrypt.hashpw(nueva_contra.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        with get_cursor(commit=True) as cur:
            cur.execute("UPDATE usuarios SET contrasena_hash = %s WHERE id = %s", (hashed, user_id))

    @staticmethod
    def actualizar_datos_basicos(user_id: int, nombre: Optional[str] = None,
                                 apellido: Optional[str] = None, email: Optional[str] = None) -> None:
        sets, params = [], []
        if nombre:   sets.append("nombre = %s");   params.append(nombre)
        if apellido: sets.append("apellido = %s"); params.append(apellido)
        if email:    sets.append("email = %s");    params.append(email)
        if not sets:
            return
        params.append(user_id)
        q = f"UPDATE usuarios SET {', '.join(sets)} WHERE id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(q, tuple(params))

    # ---------- DELETE ----------
    @staticmethod
    def eliminar_por_id(user_id: int) -> None:
        with get_cursor(commit=True) as cur:
            cur.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))

    @staticmethod
    def eliminar_por_dni(dni: int) -> None:
        with get_cursor(commit=True) as cur:
            cur.execute("DELETE FROM usuarios WHERE dni = %s", (dni,))

    # ---------- Helpers ----------
    @staticmethod
    def existe_email(email: str) -> bool:
        with get_cursor() as cur:
            cur.execute("SELECT 1 FROM usuarios WHERE email = %s LIMIT 1", (email,))
            return cur.fetchone() is not None

    @staticmethod
    def existe_dni(dni: int) -> bool:
        with get_cursor() as cur:
            cur.execute("SELECT 1 FROM usuarios WHERE dni = %s LIMIT 1", (dni,))
            return cur.fetchone() is not None
        

UsuarioDAO.actualizar_contrasena = UsuarioDAO.actualizar_contrasena_por_dni
