# src/app/servicios/dispositivos_service.py
from typing import List, Dict, Optional
from app.dao.dispositivos_dao import DispositivosDAO

class DispositivosService:
    @staticmethod
    def listar_por_usuario(user_id: int) -> List[Dict]:
        return DispositivosDAO.obtener_por_usuario(user_id)

    @staticmethod
    def crear_admin(current_user: Dict, id_habitacion: Optional[int], id_tipo: int, etiqueta: str, estado: bool=False) -> int:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede crear dispositivos.")
        return DispositivosDAO.crear(id_habitacion, id_tipo, estado, etiqueta)

    @staticmethod
    def actualizar_admin(current_user: Dict, id_dispositivo: int, **campos) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede modificar dispositivos.")
        DispositivosDAO.actualizar(id_dispositivo, **campos)

    @staticmethod
    def eliminar_admin(current_user: Dict, id_dispositivo: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede eliminar dispositivos.")
        DispositivosDAO.eliminar(id_dispositivo)
