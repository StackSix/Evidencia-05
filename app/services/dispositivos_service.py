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
    def leer(id_dispositivo: int) -> Camara | None:
        """
        Lee un solo dispositivo de tipo Cámara por su ID. La variable 'user_id'
        es un nombre de parámetro heredado del código original, pero aquí se utiliza
        para buscar por el 'id_dispositivo'.
        """
        return DispositivoDAO.leer(id_dispositivo)

    @staticmethod
    def leer_dispositivos_por_dni(dni: int) -> List[Dict]:
        """
        Llama al DAO para obtener todos los dispositivos de un usuario por su DNI.
        """
        return DispositivoDAO.leer_por_dni_usuario(dni)

    @staticmethod
    def actualizar(current_user: Dict, camara: Camara) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede modificar dispositivos.")

        if not camara or not camara.id_dispositivo:
            raise ValueError("El objeto Camara no es válido o no tiene un ID de dispositivo.")

        if not DispositivoDAO.actualizar(camara):
            raise ValueError(f"No se pudo actualizar la cámara con ID {camara.id_dispositivo}. Puede que no exista.")

    @staticmethod
    def eliminar(current_user: Dict, id_dispositivo: int) -> None:
        if current_user.get("rol") != "admin":
            raise PermissionError("Solo un admin puede eliminar dispositivos.")
        
        if not id_dispositivo:
            raise ValueError("El ID del dispositivo no puede ser nulo.")

        # El DAO devuelve un booleano, se levanta una excepción si la eliminación falla.
        if not DispositivoDAO.eliminar(id_dispositivo):
            raise ValueError(f"No se pudo eliminar el dispositivo con ID {id_dispositivo}. Puede que no exista.")