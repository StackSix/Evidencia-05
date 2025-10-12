"""Servicios de dominio relacionados con dispositivos inteligentes."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.dao.dispositivos_dao import DispositivoDAO


class DispositivosService:
    @staticmethod
    def listar_por_usuario(usuario_id: int) -> List[Dict[str, Any]]:
        return DispositivoDAO.obtener_por_usuario(usuario_id)

    @staticmethod
    def crear_admin(
        current_user: Dict,
        id_habitacion: Optional[int],
        id_tipo: int,
        etiqueta: str,
        estado: bool = False,
    ) -> int:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede crear dispositivos.")

        return DispositivoDAO.crear_dispositivo(id_habitacion, id_tipo, estado, etiqueta)

    @staticmethod
    def actualizar_admin(current_user: Dict, dispositivo_id: int, **campos: Any) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede modificar dispositivos.")

        DispositivoDAO.actualizar(dispositivo_id, **campos)

    @staticmethod
    def eliminar_admin(current_user: Dict, dispositivo_id: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede eliminar dispositivos.")

        DispositivoDAO.eliminar(dispositivo_id)