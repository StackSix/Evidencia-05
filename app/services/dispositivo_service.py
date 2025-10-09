from app.dao.dispositivos_dao import DispositivoDAO

class DispositivoService:

    @staticmethod
    def registrar_camara(usuario_id: int, nombre: str, modelo: str):
        device_id = DispositivoDAO.crear(None, "CAMARA", "OFF", usuario_id)
        DispositivoDAO.crear_camara(device_id, nombre, modelo)
        return device_id