from __future__ import annotations
from typing import Optional, List
from app.dominio.usuarios import Usuario
from app.dao.usuarios_dao import UsuarioDAO
from app.dao.dispositivos_dao import DispositivoDAO
from app.dominio.dispositivos import Dispositivo


class UsuarioService:
    def __init__(self, usuario_dao: UsuarioDAO = UsuarioDAO()):
        self.usuario_dao = usuario_dao
        self.roles_validos = {"user": 1, "admin": 2} 

    def registrar_usuario(self, dni: int, nombre: str, apellido: str, email: str, contrasena: str, rol: str = "user") -> Usuario:
        if self.usuario_dao.leer_por_email(email):
            raise ValueError(f"No se pudo completar el registro, porque el email ({email}) ya le pertenece a un usuario registrado. Por favor, verifique e intentelo nuevamente.")
        
        id_rol = self.roles_validos.get(rol)
        if not id_rol:
            raise ValueError(f"El rol '{rol}' ingresado no existe o no es válido.")
            
        self.usuario_dao.crear(dni, id_rol, nombre, apellido, email, contrasena)
        return Usuario(DNI=dni, nombre=nombre, apellido=apellido, email=email, rol=rol)

    def obtener_usuario_por_dni(self, dni: int) -> Optional[Usuario]:
        usuario_dict = self.usuario_dao.leer(dni)
        if usuario_dict:
            return Usuario(
                DNI=usuario_dict['dni'],
                nombre=usuario_dict['nombre'],
                apellido=usuario_dict['apellido'],
                email=usuario_dict['email'],
                rol=usuario_dict['rol']
            )
        return None
        
    def actualizar_rol(self, dni: int, nuevo_rol: str) -> bool:
        nuevo_id_rol = self.roles_validos.get(nuevo_rol)
        if not nuevo_id_rol:
            raise ValueError(f"El rol '{nuevo_rol}' no es válido.")
            
        return self.usuario_dao.actualizar(dni, nuevo_id_rol)
    
    def eliminar_usuario(self, dni: int) -> bool:
        return self.usuario_dao.eliminar(dni)
    
    def iniciar_sesion(self, email: str, contrasena: str) -> Optional[Usuario]:
        "Método para verificar credenciales."
        if self.usuario_dao.verificar_contrasena(email, contrasena):
            usuario_dict = self.usuario_dao.leer_por_email(email)
            if usuario_dict:
                return Usuario(
                    DNI=usuario_dict['dni'],
                    nombre=usuario_dict['nombre'],
                    apellido=usuario_dict['apellido'],
                    email=usuario_dict['email'],
                    rol=usuario_dict['rol']
                )
        return None
    
    def consultar_dispositivos_por_dni(self, dni: int) -> List[Dispositivo]:
        "Consulta los dispositivos asociados a un usuario por su DNI."
        
        dispositivos_lista_de_dicts = self.dispositivo_dao.leer_por_dni_usuario(dni)
        return [
            Dispositivo(
                id_dispositivo=d['id'],
                nombre=d['nombre'],
                estado=d['estado'],
                dni_usuario=d['dni_usuario']
            ) for d in dispositivos_lista_de_dicts
        ]