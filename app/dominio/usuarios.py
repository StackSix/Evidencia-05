from __future__ import annotations
import re
import bcrypt
from typing import List
from app.dominio.domicilio import Domicilio
from app.servicios.gestor_domicilio import GestorDomicilio


class Usuario:
    def __init__(self, id_usuario: int, dni: int, nombre: str, apellido: str, email: str, contrasena: str, rol: str = "Usuario",  gestor_domicilios: GestorDomicilio = None) -> None:
        if not nombre or len(nombre) < 2:
            raise ValueError("Nombre inválido.")
        self.__id_usuario = id_usuario
        self.__dni = dni
        self.__nombre = nombre
        self.__apellido = apellido
        self.__email = email
        self.__contrasena = contrasena
        self.__rol = rol
        self.__gestor_domicilios = gestor_domicilios if gestor_domicilios is not None else GestorDomicilio()
    
    @property
    def id_usuario(self) -> int:
        return self.__id_usuario
    
    @property     
    def dni(self) -> int:
        return self.__dni
    
    @dni.setter
    def dni(self, dni_correcto):
        if not isinstance(dni_correcto, int):
            raise TypeError("El DNI debe ser un numero entero.")
        dni_str = str(dni_correcto)
        
        if len(dni_str) != 8 and len(dni_str) != 7:
            raise ValueError("El DNI debe tener 7 u 8 numeros.")
        self.__dni = dni_correcto
        
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre):
        if not isinstance(nuevo_nombre, str) or len(nuevo_nombre) < 2:
            raise TypeError("El nombre no es válido.")
        self.__nombre = nuevo_nombre
        
    @property
    def apellido(self) -> str:
        return self.__apellido
    
    @apellido.setter
    def apellido(self, nuevo_apellido):
        if not isinstance(nuevo_apellido, str) or len(nuevo_apellido) < 2:
            raise TypeError("El apellido no es válido.")
        self.__apellido = nuevo_apellido
    
    @property 
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, nuevo_email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, nuevo_email):
            raise ValueError(f"Email '{nuevo_email}' inválido.")
        self.__email = nuevo_email
        
    @property
    def contrasena(self) -> str:
        return self.__contrasena
    
    @contrasena.setter
    def contrasena(self, nueva_contrasena):
        if len(nueva_contrasena) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not any(c.isdigit() for c in nueva_contrasena):
            raise ValueError("La contraseña debe contener al menos un número")
        
        # Encriptar y guardar
        hashed = bcrypt.hashpw(nueva_contrasena.encode("utf-8"), bcrypt.gensalt())
        self.__contrasena = hashed.decode("utf-8")
        
    @property
    def rol(self) -> str:
        return self.__rol
    
    @rol.setter
    def rol(self, nuevo_rol):
        ROLES_PERMITIDOS = ["admin", "user"]
        
        if nuevo_rol not in ROLES_PERMITIDOS:
            raise ValueError("El rol ingresado no es valido.")
        self.__rol = nuevo_rol
    
    @property        
    def gestor_domicilios(self) -> GestorDomicilio:
        return self.__gestor_domicilios
       
    def consultar_datos_personales(self):
        return f"DNI: {self.dni}\n Nombre: {self.nombre}\n Apellido: {self.apellido}\n Email: {self.email}\n Rol: {self.rol}"
