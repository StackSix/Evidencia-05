from __future__ import annotations
from typing import List, Optional
import bcrypt
from dominio.usuario import Usuario
from dao.usuario_dao import UsuarioDAO
from modulos_main.funcion_autenticacion import validar_email

class GestorUsuario:
    """Gestiona la lógica de negocio de los usuarios, con lista en memoria y sincronización con DB."""
    
    def __init__(self, usuarios: Optional[List[Usuario]] = None):
        try:
            self.__usuarios = usuarios if usuarios is not None else UsuarioDAO.listar_todos_usuarios()
        except ValueError as e:
            print(f"⚠️ Advertencia al cargar usuarios: {e}")
            self.__usuarios = []
    
    @staticmethod
    def registrar_usuario(dni: int, nombre: str, apellido: str, email: str, contrasena: str, rol: str = "Usuario") -> int:
        if len(contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")
        
        validar_email(email)
        
        existente = UsuarioDAO.obtener_por_email(email)
        if existente:
            raise ValueError("Ya existe un usuario con ese email.")
        
        id_usuario = UsuarioDAO.registrar_usuario(dni, nombre, apellido, email, contrasena, rol)
        print(f"✅ Usuario creado con ID {id_usuario}.")

    @staticmethod
    def login(email: str, contrasena_plana: str) -> Optional[dict]:
        rec = UsuarioDAO.obtener_por_email(email)
        if not rec:
            return None
        hashed = rec.pop("contrasena", None)
        if not hashed:
            return None
        ok = bcrypt.checkpw(contrasena_plana.encode("utf-8"), hashed.encode("utf-8"))
        return rec if ok else None

    def agregar_usuario(self, dni: int, nombre: str, apellido: str, email: str, contrasena: str, rol: str = "Usuario") -> None:
        try:
            validar_email(email)
            UsuarioDAO.registrar_usuario(dni, nombre, apellido, email, contrasena, rol)
            self.__usuarios = UsuarioDAO.listar_todos_usuarios()
            print("✅ Usuario registrado correctamente.")
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")

    def actualizar_usuario(self, id_usuario: int, email: str, nombre: str, apellido: str, contrasena: str) -> None:
        try:
            validar_email(email)
            actualizado = UsuarioDAO.actualizar_usuario(id_usuario, email, nombre, apellido, contrasena)
            if actualizado:
                usuario = next((u for u in self.__usuarios if u.id_usuario == id_usuario), None)
                if usuario:
                    usuario.nombre = nombre
                    usuario.apellido = apellido
                    usuario.email = email
                print("✅ Usuario actualizado correctamente.")
            else:
                print(f"⚠️ No se encontró ningún usuario con ID {id_usuario}. No se realizaron cambios.")
        except Exception as e:
            print(f"❌ Error al actualizar usuario: {e}")

    def modificar_rol(self, id_usuario: int, nuevo_rol: str) -> None:
        modificado = UsuarioDAO.modificar_rol(id_usuario, nuevo_rol)
        if modificado:
            for u in self.__usuarios:
                if getattr(u, "id_usuario", None) == id_usuario:
                    setattr(u, "rol", nuevo_rol)
                    break
            print("✅ Rol modificado correctamente.")
        else:
            print("⚠️ No se pudo modificar el rol.")

    def eliminar_usuario(self, id_usuario: int) -> None:
        eliminado = UsuarioDAO.eliminar_usuario(id_usuario)
        if eliminado:
            self.__usuarios = [u for u in self.__usuarios if getattr(u, "id_usuario", None) != id_usuario]
            print("✅ Usuario eliminado correctamente.")
        else:
            print("⚠️ No se encontró ningún usuario con ese ID.")

    def listar_usuarios(self) -> List[Usuario]:
        if not self.__usuarios:
            print("❌ No hay usuarios registrados.")
            return []
        for u in self.__usuarios:
            print(f"ID: {u.id_usuario} - DNI: {u.dni} - NOMBRE: {u.nombre} - APELLIDO: {u.apellido} - EMAIL: {u.email} - ROL: {u.rol}")
        return self.__usuarios

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        for u in self.__usuarios:
            if u.email == email:
                return u
        return None

    @property
    def usuarios(self) -> List[Usuario]:
        return self.__usuarios
    