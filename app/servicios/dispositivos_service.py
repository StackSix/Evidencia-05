from __future__ import annotations
from typing import Dict, Optional, List
from app.dao.dispositivos_dao import DispositivoDAO

class DispositivosService:
    # común (usuario)
    @staticmethod
    def listar_por_usuario(user_id: int) -> List[dict]:
        return DispositivoDAO.listar_por_usuario(user_id)

    # admin
    @staticmethod
    def listar_admin(current_user: Dict) -> List[dict]:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo admin.")
        return DispositivoDAO.listar_todos()

    @staticmethod
    def crear_admin(current_user: Dict, id_habitacion: Optional[int], id_tipo: int, etiqueta: str) -> int:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo admin.")
        if not etiqueta or len(etiqueta) < 3:
            raise ValueError("Etiqueta inválida.")
        return DispositivoDAO.crear(id_habitacion, id_tipo, etiqueta)

    @staticmethod
    def actualizar_admin(current_user: Dict, id_dispositivo: int,
                         id_habitacion: Optional[int] = None,
                         id_tipo: Optional[int] = None,
                         etiqueta: Optional[str] = None) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo admin.")
        DispositivoDAO.actualizar(id_dispositivo, id_habitacion=id_habitacion,
                                  id_tipo=id_tipo, etiqueta=etiqueta)

    @staticmethod
    def set_estado_admin(current_user: Dict, id_dispositivo: int, encender: bool) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo admin.")
        DispositivoDAO.set_estado(id_dispositivo, encender)

    @staticmethod
    def eliminar_admin(current_user: Dict, id_dispositivo: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo admin.")
        DispositivoDAO.eliminar(id_dispositivo)
