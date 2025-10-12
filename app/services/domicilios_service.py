from typing import List, Dict
from app.dao.domicilios_dao import DomiciliosDAO

class DomiciliosService:
    @staticmethod
    def crear_domicilio_admin(current_user: Dict, direccion: str, numeracion: str, ciudad: str, nombre_domicilio: str) -> int:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede crear domicilios.")
        return DomiciliosDAO.crear(direccion, numeracion, ciudad, nombre_domicilio)

    @staticmethod
    def vincular_usuario_domicilio_admin(current_user: Dict, dni: int, id_hogar: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede vincular usuarios a domicilios.")
        DomiciliosDAO.vincular_usuario(dni, id_hogar)
        
    @staticmethod
    def listar_domicilio_usuario(dni: int) -> List[Dict]:
        return DomiciliosDAO.leer(dni)
        
    @staticmethod
    def actualizar_domicilio(current_user: Dict, dni: int, id_hogar: int, direccion: str, numeracion: str, ciudad: str, alias_domicilio: str) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede modificar un domicilio.")
        DomiciliosDAO.actualizar(dni, id_hogar, direccion, numeracion, ciudad, alias_domicilio)
        
    @staticmethod
    def eliminar_domicilio(current_user: Dict, dni: int, id_hogar: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede eliminar un domicilio.")
        DomiciliosDAO.eliminar(dni, id_hogar)
        