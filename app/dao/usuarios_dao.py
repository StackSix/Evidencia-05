import mysql.connector
from __future__ import annotations
from typing import Optional, List, Dict
import bcrypt
from app.conn.cursor import get_cursor
from mysql.connector import Error
from app.conn.logger import logger
from interfaz_dao import DataAccessDAO
from app.dominio.usuarios import Usuario

class UsuarioDAO(DataAccessDAO):
    "DAO para 'usuarios' con FK a 'roles'"
    @staticmethod
    def crear(dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena: str) -> None:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO usuarios (dni, id_rol, nombre, apellido, email, contrasena)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (id_rol, nombre, apellido, email, hashed))
        except mysql.connector.Error as e:
            logger.exception("No se pudo registrar el usuario en la Base de Datos.")
            raise e
        
    @staticmethod
    def leer(dni: int) -> Optional[Dict]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT u.dni, u.nombre, u.apellido, u.email, u.contrasena, r.nombre AS rol
                    FROM usuarios u
                    JOIN roles r ON r.id = u.id_rol
                    WHERE u.dni = %s
                """
                cursor.execute(query, (dni,))
                return cursor.fetchone()
        except mysql.connector.Error as e:
            logger.exception("No se pudo obtener el usuario buscado.")
            raise e
        
    @staticmethod
    def leer_por_email(email: str) -> Optional[Dict]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT u.dni, u.nombre, u.apellido, u.email, u.contrasena, r.nombre AS rol
                    FROM usuarios u
                    JOIN roles r ON r.id = u.id_rol
                    WHERE u.email = %s
                """
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except mysql.connector.Error as e:
            logger.exception("No se pudo obtener el usuario buscado.")
            raise e
    
    @staticmethod
    def leer_por_nombre(nombre: str) -> List[Dict]:
        "Busca usuarios por su nombre y devuelve una lista de diccionarios."
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT u.dni, u.nombre, u.apellido, u.email, u.contrasena, r.nombre AS rol
                    FROM usuarios u
                    JOIN roles r ON r.id = u.id_rol
                    WHERE u.nombre = %s
                """
                cursor.excute(query, (nombre,))
                rows = cursor.fetchall()
                return rows
        except mysql.connector.Error as e:
            logger.exception("No se pudo obtener el usuario buscado.")
            raise e
        
    @staticmethod
    def actualizar(dni: int, nuevo_id_rol: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE usuarios 
                    SET id_rol = %s 
                    WHERE dni = %s"""
                cursor.execute(query, (nuevo_id_rol, dni))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error: no se pudo modificar el rol del usuario.")
            raise e
        
    @staticmethod
    def eliminar(dni: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    DELETE FROM usuarios 
                    WHERE dni = %s
                """
                cursor.execute(query, (dni,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar eliminar el usuario.")
            raise e
        
    """
    @staticmethod
    def obtener_por_email(email: str, incluir_hash: bool = False) -> Optional[Dict]:
        
        incluir_hash=True si se necesita validar contraseña (login).
        
        if incluir_hash:
            query = 
                SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email, u.contrasena, r.nombre AS rol
                FROM usuarios u
                JOIN roles r ON r.id = u.id_rol
                WHERE u.email = %s
            
        else:
            query = 
                SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email, r.nombre AS rol
                FROM usuarios u
                JOIN roles r ON r.id = u.id_rol
                WHERE u.email = %s
            
        with get_cursor() as cur:
            cur.execute(query, (email,))
            return cur.fetchone()

    @staticmethod
    def obtener_todos() -> List[Dict]:
        query = 
            SELECT u.id, u.dni, u.id_rol, u.nombre, u.apellido, u.email, r.nombre AS rol
            FROM usuarios u
            JOIN roles r ON r.id = u.id_rol
            ORDER BY u.id
        
        with get_cursor() as cur:
            cur.execute(query)
            return cur.fetchall()
    """
    

    """
    @staticmethod
    def actualizar_contrasena(usuario_id: int, contrasena: str) -> None:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = "UPDATE usuarios SET contrasena = %s WHERE id = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (hashed, usuario_id))

    @staticmethod
    def actualizar_contrasena_por_dni(dni: int, contrasena: str) -> None:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = "UPDATE usuarios SET contrasena = %s WHERE dni = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (hashed, dni))
    """
    """        
    @staticmethod
    def eliminar_por_dni(dni: int) -> None:
        query = "DELETE FROM usuarios WHERE dni = %s"
        with get_cursor(commit=True) as cur:
            cur.execute(query, (dni,))
    """

