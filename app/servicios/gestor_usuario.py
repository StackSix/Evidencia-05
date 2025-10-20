from __future__ import annotations
from typing import List, Optional
from app.dominio.usuarios import Usuario
from app.dao.usuarios_dao import UsuarioDAO

class GestorUsuario:
    """Gestiona la lógica de negocio de los usuarios, con lista en memoria y sincronización con DB."""
    
    def __init__(self, usuarios: Optional[List[Usuario]] = None):
        self.__usuarios = usuarios if usuarios is not None else UsuarioDAO.listar_todos_usuarios()

    def agregar_usuario(self, dni: int, id_rol: int, nombre: str, apellido: str, email: str, contrasena: str) -> None:
        try:
            UsuarioDAO.registrar_usuario(dni, id_rol, nombre, apellido, email, contrasena)
            self.__usuarios = UsuarioDAO.listar_todos_usuarios()
            print("✅ Usuario registrado correctamente.")
        except Exception as e:
            print(f"❌ Error al registrar usuario: {e}")

    def actualizar_usuario(self, email: str, nombre: str, apellido: str, contrasena: str) -> None:
        actualizado = UsuarioDAO.actualizar_usuario(email, nombre, apellido, contrasena)
        if actualizado:
            # actualizar en memoria
            usuario = self.obtener_usuario_por_email(email)
            if usuario:
                usuario.nombre = nombre
                usuario.apellido = apellido
            print("✅ Usuario actualizado correctamente.")
        else:
            print("⚠️ No se encontró ningún usuario con ese email.")

    def modificar_rol(self, id_usuario: int, nuevo_id_rol: int) -> None:
        modificado = UsuarioDAO.modificar_rol(id_usuario, nuevo_id_rol)
        if modificado:
            print("✅ Rol modificado correctamente.")
        else:
            print("⚠️ No se pudo modificar el rol.")

    def eliminar_usuario(self, id_usuario: int) -> None:
        eliminado = UsuarioDAO.eliminar_usuario(id_usuario)
        if eliminado:
            self.__usuarios = [u for u in self.__usuarios if getattr(u, "dni", None) != id_usuario]
            print("✅ Usuario eliminado correctamente.")
        else:
            print("⚠️ No se encontró ningún usuario con ese ID.")

    def listar_usuarios(self) -> None:
        if not self.__usuarios:
            print("❌ No hay usuarios registrados.")
            return
        for u in self.__usuarios:
            print(f"{u.dni} - {u.nombre} - {u.apellido} - {u.email} - {u.rol}")

    def obtener_usuario_por_email(self, email: str) -> Optional[Usuario]:
        for u in self.__usuarios:
            if u.email == email:
                return u
        return None

    @property
    def usuarios(self) -> List[Usuario]:
        return self.__usuarios
    