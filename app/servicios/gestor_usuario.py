from __future__ import annotations
from typing import List, Optional
from dominio.usuarios import Usuario
from dao.usuarios_dao import UsuarioDAO
from modulos_main.funciones_de_autenticacion import validar_email

class GestorUsuario:
    """Gestiona la lógica de negocio de los usuarios, con lista en memoria y sincronización con DB."""
    
    def __init__(self, usuarios: Optional[List[Usuario]] = None):
        try:
            self.__usuarios = usuarios if usuarios is not None else UsuarioDAO.listar_todos_usuarios()
        except ValueError as e:
            print(f"⚠️ Advertencia al cargar usuarios: {e}")
            self.__usuarios = []

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
    