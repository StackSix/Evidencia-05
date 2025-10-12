from __future__ import annotations
import re

class Usuario:
    def __init__(self, DNI: int, nombre: str, apellido: str, email: str, rol: str = "user") -> None:
        if not nombre or len(nombre) < 2:
            raise ValueError("Nombre inválido.")
        self.__DNI = DNI
        self.nombre = nombre
        self.apellido = apellido
        self.__email = email
        self.__rol = rol
    
    @property     
    def DNI(self)-> int:
        return self.__DNI 
    
    @DNI.setter
    def DNI(self, DNI_correcto)-> int:
        "Setter para modificar DNI incorrecto con validación."
        if not isinstance(DNI_correcto, int):
            raise TypeError("El DNI debe ser un numero entero.")
        dni_str = str(DNI_correcto)
        
        if len(dni_str) != 8 and len(dni_str) != 7:
            raise ValueError("El DNI debe tener 7 u 8 numeros.")
        self.__DNI = DNI_correcto
    
    @property 
    def email(self)-> str:
        return self.__email
    
    @email.setter
    def email(self, nuevo_email)-> str:
        "Setter para actualizar el email."
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(regex, nuevo_email):
            raise ValueError(f"Email '{nuevo_email}' inválido.")
        self.__email = nuevo_email
        
    @property
    def rol(self)-> str:
        return self.__rol
    
    @rol.setter
    def rol(self, nuevo_rol)-> str:
        ROLES_PERMITIDOS = ["admin", "user"]
        
        if nuevo_rol not in ROLES_PERMITIDOS:
            raise ValueError("El rol ingresado no es valido.")
        self.__rol = nuevo_rol
        
    def consultar_datos_personales(self):
        return f"DNI: {self.DNI}\n Nombre: {self.nombre}\n Apellido: {self.apellido}\n Email: {self.email}\n Rol: {self.rol}"
    