# src/app/servicios/habitacion_service.py
from typing import List, Dict
from app.dao.habitacion_dao import HabitacionDAO

class HabitacionService:
    @staticmethod
    def listar_por_hogar(hogar_id: int) -> List[Dict]:
        return HabitacionDAO.obtener_por_hogar(hogar_id)

    @staticmethod
    def crear_admin(current_user: Dict, hogar_id: int, nombre_habitacion: str) -> int:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede crear habitaciones.")
        return HabitacionDAO.crear(hogar_id, nombre_habitacion)
