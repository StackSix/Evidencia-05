from abc import ABC, abstractmethod
from typing import Optional, Any, List
from app.dominio.automatizacion import Automatizacion

class IAutomatizacionDAO(ABC):
    @abstractmethod
    def registrar_automatizacion(automatizacion: Automatizacion) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def obtener_automatizacion(id_automatizacion: int) -> Optional[Any]:  
        raise NotImplementedError
    
    @abstractmethod
    def obtener_todas() -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    def obtener_automatizaciones_por_domicilio(id_domicilio: int) -> Optional[Any]:
        raise NotImplementedError
    
    @abstractmethod
    def actualizar_automatizacion(automatizacion: Automatizacion) -> bool:  
        raise NotImplementedError
    
    @abstractmethod
    def eliminar_automatizacion(id_automatizacion: int) -> bool:  
        raise NotImplementedError
    