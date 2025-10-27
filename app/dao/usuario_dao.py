from __future__ import annotations
import mysql.connector
from typing import Optional, List, Dict
import bcrypt
from app.conn.cursor import get_cursor
from app.conn.logger import logger
from app.dao.interfaces.i_usuario_dao import IUsuarioDAO
from app.dominio.usuario import Usuario

class UsuarioDAO(IUsuarioDAO):
    @staticmethod
    def registrar_usuario(dni: int, nombre: str, apellido: str, email: str, contrasena: str, rol: str) -> int:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    INSERT INTO usuario (dni, nombre, apellido, email, contrasena, rol) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (dni, nombre, apellido, email, hashed, rol)) 
                return cursor.lastrowid
        except mysql.connector.Error as e:
            logger.exception("No se pudo registrar el usuario en la Base de Datos.")
            raise e
    
    @staticmethod
    def listar_todos_usuarios() -> List[Usuario]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT u.id_usuario, u.dni, u.nombre, u.apellido, u.email, u.contrasena, u.rol
                    FROM usuario u
                    ORDER BY u.id_usuario
                """
                cursor.execute(query)
                rows = cursor.fetchall()

            usuarios = []
            for row in rows:
                nombre = row["nombre"]
                if not nombre or len(nombre) < 2:
                    logger.warning(f"Nombre inválido para id_usuario={row['id_usuario']}. Se reemplazará por 'Usuario{row['id_usuario']}'")
                    nombre = f"Usuario{row['id_usuario']}"

                usuarios.append(
                    Usuario(
                        id_usuario=row["id_usuario"],
                        dni=row["dni"],
                        nombre=nombre,  
                        apellido=row["apellido"],
                        email=row["email"],
                        contrasena=row["contrasena"],
                        rol=row["rol"]
                    )
                )

            return usuarios

        except mysql.connector.Error as e:
            logger.exception("No se pudieron obtener los usuarios registrados.")
            raise e
        
    @staticmethod 
    def obtener_por_dni(dni: int) -> Optional[Dict]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT u.id_usuario, u.dni, u.nombre, u.apellido, u.email, u.contrasena, u.rol
                    FROM usuario u
                    WHERE u.dni = %s
                """
                cursor.execute(query, (dni,))
                return cursor.fetchone()
        except mysql.connector.Error as e:
            logger.exception("No se pudo obtener el usuario buscado por dni.")
            raise e
        
    @staticmethod
    def obtener_por_email(email: str) -> Optional[Dict]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT u.id_usuario, u.dni, u.nombre, u.apellido, u.email, u.contrasena, u.rol
                    FROM usuario u
                    WHERE u.email = %s
                """
                cursor.execute(query, (email,))
                return cursor.fetchone()
        except mysql.connector.Error as e:
            logger.exception("No se pudo obtener el usuario buscado por email.")
            raise e
    
    @staticmethod
    def actualizar_usuario(id_usuario, email: str, nombre: str, apellido: str, contrasena: str) -> bool:
        hashed = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE usuario
                    SET email = %s, nombre = %s, apellido = %s, contrasena = %s
                    WHERE id_usuario = %s
                """
                cursor.execute(query, (email, nombre, apellido, hashed, id_usuario))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error: no se pudo actualizar el usuario.")
            raise e
        
    @staticmethod
    def modificar_rol(id_usuario: int, nuevo_rol: str) -> bool:
        ROLES_VALIDOS = ["Admin", "Usuario"]
        if nuevo_rol not in ROLES_VALIDOS:
            raise ValueError(f"El rol '{nuevo_rol}' no es válido. Debe ser 'Admin' o 'Usuario'.")

        try:
            with get_cursor(commit=True) as cursor:
                query = """
                    UPDATE usuario
                    SET rol = %s
                    WHERE id_usuario = %s
                """
                cursor.execute(query, (nuevo_rol, id_usuario))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error: no se pudo modificar el rol del usuario.")
            raise e
        
    @staticmethod
    def eliminar_usuario(id_usuario: int) -> bool:
        try:
            with get_cursor(commit=True) as cursor:
                query = "DELETE FROM usuario WHERE id_usuario = %s"
                cursor.execute(query, (id_usuario,))
                return cursor.rowcount > 0
        except mysql.connector.Error as e:
            logger.exception("Error al intentar eliminar el usuario.")
            raise e
        