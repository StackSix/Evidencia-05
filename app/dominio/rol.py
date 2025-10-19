class Rol:
    """Clase para manejar los roles de usuarios."""

    def __init__(self, id_rol, nombre):
        self.__id_rol = id_rol
        self.__nombre = nombre
        
    @property
    def id_rol(self) -> int:
        return self.__id_rol
    
    @property
    def nombre(self) -> str:
        return self.__nombre