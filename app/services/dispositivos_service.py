from typing import List, Dict, Optional
from app.dao.dispositivos_dao import DispositivoDAO
from app.dominio.dispositivos import Dispositivo
from app.dominio.camaras import Camara

class DispositivosService:
    @staticmethod
    def crear(current_user: Dict, id_habitacion: int, accion: str, estado: str, nombre_camara: str, grabacion_modo: str = "AUTO", estado_automatizacion: bool = False) -> Camara | None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede crear dispositivos.")
        
        return DispositivoDAO.crear(id_habitacion, accion, estado, nombre_camara, grabacion_modo, estado_automatizacion)

    @staticmethod
    def leer(user_id: int) -> Camara | None:
        """
        Este método ahora lee un solo dispositivo por su ID, no por el ID de usuario.
        """
        return DispositivoDAO.leer(user_id)

    @staticmethod
    def leer_dispositivos_por_dni(dni: int) -> List[Dict]:
        """
        Llama al DAO para obtener todos los dispositivos de un usuario por su DNI.
        """
        # La lógica de validación de usuario (si es el dueño, etc.) iría aquí.
        # Por ahora, solo delegamos la llamada al DAO.
        return DispositivoDAO.leer_por_dni_usuario(dni)

    @staticmethod
    def actualizar(current_user: Dict, camara: Camara) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede modificar dispositivos.")
        DispositivoDAO.actualizar(camara)

    @staticmethod
    def eliminar(current_user: Dict, id_dispositivo: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede eliminar dispositivos.")
        DispositivoDAO.eliminar(id_dispositivo)