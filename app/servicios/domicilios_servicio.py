# src/app/servicios/domicilios_service.py
from typing import List, Dict
from app.dao.domicilios_dao import DomiciliosDAO

class DomiciliosService:
    @staticmethod
    def listar_por_usuario(user_id: int) -> List[Dict]:
        return DomiciliosDAO.obtener_por_usuario(user_id)

    @staticmethod
    def crear_admin(current_user: Dict, direccion: str, numeracion: str, ciudad: str, nombre_domicilio: str) -> int:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede crear domicilios.")
        return DomiciliosDAO.crear(direccion, numeracion, ciudad, nombre_domicilio)

    @staticmethod
    def vincular_usuario_admin(current_user: Dict, user_id: int, hogar_id: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede vincular usuarios a domicilios.")
        DomiciliosDAO.vincular_usuario(user_id, hogar_id)
