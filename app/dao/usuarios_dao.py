# src/app/dao/usuario_dao.py
from __future__ import annotations
from typing import Optional, List, Dict
import bcrypt
from app.conn.cursor import get_cursor

class UsuarioDAO:
    """
    DAO para `usuarios` con FK a `roles`.
    columnas sugeridas en `usuarios`:
      id (PK), dni (UNQ), id_rol (FK roles.id), nombre, apellido, email (UNQ), contrasena (hash)
    """

    # ---------- CREATE ----------
    @staticmethod
    def crear_usuario(dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena: str) -> int:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = """
            INSERT INTO usuarios (dni, id_rol, nombre, apellido, email, contrasena)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with get_cursor(commit=True) as cur:
            cur.execute(query, (dni, id_rol, nombre, apellido, email, hashed))
            return cur.lastrowid

    # ---------- READ ----------
    @staticmethod
    def obtener_por_dni(dni: int) -> Optional[Dict]:
        query = """
            SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email, r.nombre AS rol
            FROM usuarios u
            JOIN roles r ON r.id = u.id_rol
            WHERE u.dni = %s
        """
        with get_cursor() as cur:
            cur.execute(query, (dni,))
            return cur.fetchone()

    @staticmethod
    def obtener_por_email(email: str, incluir_hash: bool = False) -> Optional[Dict]:
        """
        incluir_hash=True si se necesita validar contraseña (login).
        """
        if incluir_hash:
            query = """
                SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email, u.contrasena, r.nombre AS rol
                FROM usuarios u
                JOIN roles r ON r.id = u.id_rol
                WHERE u.email = %s
            """
        else:
            query = """
                SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email, r.nombre AS rol
                FROM usuarios u
                JOIN roles r ON r.id = u.id_rol
                WHERE u.email = %s
            """
        with get_cursor() as cur:
            cur.execute(query, (email,))
            return cur.fetchone()

    @staticmethod
    def obtener_todos() -> List[Dict]:
        query = """
            SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email, r.nombre AS rol
            FROM usuarios u
            JOIN roles r ON r.id = u.id_rol
            ORDER BY u.id
        """
        with get_cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

    # ---------- UPDATE ----------
    @staticmethod
    def cambiar_rol(usuario_id: int, nuevo_id_rol: int) -> None:
        query = "UPDATE usuarios SET id_rol = %s WHERE id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (nuevo_id_rol, usuario_id))

    @staticmethod
    def obtener_id_rol_por_nombre(nombre: str) -> Optional[int]:
        q = "SELECT id_rol FROM rol WHERE nombre = %s"
        with get_cursor() as cur:
            cur.execute(q, (nombre,))
            row = cur.fetchone()
            return row["id_rol"] if row else None

    @staticmethod
    def actualizar_contrasena(dni: int, contrasena: str) -> None:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = "UPDATE usuarios SET contrasena = %s WHERE dni = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (hashed, dni))

    # ---------- DELETE ----------
    @staticmethod
    def eliminar_por_id(usuario_id: int) -> None:
        query = "DELETE FROM usuarios WHERE id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (usuario_id,))

    @staticmethod
    def eliminar_por_dni(dni: int) -> None:
        query = "DELETE FROM usuarios WHERE dni = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (dni,))

    # ---------- CASOS DE USO ----------
    @staticmethod
    def registrar(dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena: str) -> int:
        # evitar duplicado por email o dni
        if UsuarioDAO.obtener_por_email(email):
            raise ValueError("Ya existe un usuario con ese email.")
        if UsuarioDAO.obtener_por_dni(dni):
            raise ValueError("Ya existe un usuario con ese DNI.")
        return UsuarioDAO.crear_usuario(dni, id_rol, nombre, apellido, email, contrasena)

    @staticmethod
    def iniciar_sesion(email: str, contrasena_plana: str) -> Optional[Dict]:
        rec = UsuarioDAO.obtener_por_email(email, incluir_hash=True)
        if not rec:
            return None
        hashed = rec.pop("contrasena", None)
        if not hashed:
            return None
        ok = bcrypt.checkpw(contrasena_plana.encode("utf-8"), hashed.encode("utf-8"))
        return rec if ok else None
