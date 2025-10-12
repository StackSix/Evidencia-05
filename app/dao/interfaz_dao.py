from abc import ABC, abstractmethod

class DataAccessDAO(ABC):
    @abstractmethod
    def crear(self, object):
        pass
    
    @abstractmethod
    def leer(self, id: int):
        pass
    """
    @abstractmethod
    def leer_todo(self):
        pass
    """
    @abstractmethod
    def actualizar(self, object):
        pass
    
    @abstractmethod
    def eliminar(self, object):
        pass
    