import mysql.connector
from __future__ import annotations
from typing import Optional, List, Dict
import bcrypt
from app.conn.cursor import get_cursor
from mysql.connector import Error
from app.conn.logger import logger
from app.dao.interfaces.i_usuario_dao import IUsuaioDAO
from app.dominio.usuarios import Usuario

class UsuarioDAO(IUsuaioDAO):
    "DAO para 'usuarios' con FK a 'roles'"
    @staticmethod
    def registrar_usuario(dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena: str) -> None:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO usuarios (dni, id_rol, nombre, apellido, email, contrasena)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (dni, id_rol, nombre, apellido, email, hashed))
        except mysql.connector.Error as e:
            logger.exception("No se pudo registrar el usuario en la Base de Datos.")
            raise e
    
    @staticmethod
    def listar_todos_usuarios() -> List[Usuario]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT u.dni, u.nombre, u.apellido, u.email, u.contrasena, r.nombre AS rol
                    FROM usuarios u
                    JOIN roles r ON r.id = u.id_rol
                    ORDER BY u.dni
                """
                cursor.execute(query)
                rows = cursor.fetchall()
            usuarios = []
            for row in rows:
                usuarios.append(
                    Usuario(
                    dni=row["dni"],
                    nombre=row["nombre"],
                    apellido=row["apellido"],
                    email=row["email"],
                    contrasena=row["contrasena"],
                    rol=row["rol"]
                )
            )
            return usuarios
        except mysql.connector.Error as e:
            logger.exception("No se pudieron obtener los usuario registrados.")
            raise e
        
    @staticmethod #ver si se usa
    def obtener_por_dni(dni: int) -> Optional[Dict]:
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
    def obtener_por_email(email: str) -> Optional[Dict]:
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
    def actualizar_usuario(email: str, nombre: str, apellido: str, contrasena: str) -> None:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE usuarios 
                    SET nombre = %s, apellido = %s, contrasena = %s
                    WHERE email = %s"""
                cursor.execute(query, (nombre, apellido, contrasena, email))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error: no se pudo actualizar el usuario.")
            raise e
        
    @staticmethod
    def modificar_rol(id_usuario: int, nuevo_id_rol: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE usuarios 
                    SET id_rol = %s 
                    WHERE id_usuario = %s"""
                cursor.execute(query, (nuevo_id_rol, id_usuario,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error: no se pudo modificar el rol del usuario.")
            raise e
        
    @staticmethod
    def eliminar_usuario(id_usuario: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    DELETE FROM usuarios 
                    WHERE id_usuario = %s
                """
                cursor.execute(query, (id_usuario,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar eliminar el usuario.")
            raise e
    
    @staticmethod #ver si se usa
    def verificar_contrasena(email: str, contrasena: str) -> bool:
        " Verifica la contraseña de un usuario."
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = "SELECT contrasena FROM usuarios WHERE email = %s"
                cursor.execute(query, (email,))
                usuario = cursor.fetchone()
                if usuario:
                    return bcrypt.checkpw(contrasena.encode("utf-8"), usuario['contrasena'].encode("utf-8"))
                return False
        except mysql.connector.Error as e:
            logger.exception("Error al verificar la contraseña.")
            return False
        