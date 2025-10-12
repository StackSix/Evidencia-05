# src/app/servicios/habitacion_service.py
from typing import List, Dict
from app.dao.habitacion_dao import HabitacionDAO

class HabitacionService:

    @staticmethod
    def crear_admin(current_user: Dict, id_hogar: int, nombre_habitacion: str) -> int:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede crear habitaciones.")
        return HabitacionDAO.crear(id_hogar, nombre_habitacion)
    
    @staticmethod
    def listar_por_hogar(id_hogar: int) -> List[Dict]:
        return HabitacionDAO.leer(id_hogar)
    
    @staticmethod
    def modificar_habitacion(current_user: Dict, id_habitacion: int, nombre_habitacion: str) -> bool:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede modificar habitaciones.")
        return HabitacionDAO.actualizar(id_habitacion, nombre_habitacion)
    
    @staticmethod
    def borrar_habitacion(current_user: Dict, id_habitacion: int) -> bool:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede eliminar habitaciones.")
        return HabitacionDAO.eliminar(id_habitacion)
    