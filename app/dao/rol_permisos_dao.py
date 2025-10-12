from typing import List
from interfaz_dao import DataAccessDAO
from app.conn.cursor import get_cursor
import mysql.connector
from mysql.connector import Error
from app.conn.logger import logger
from app.dominio.permisos import Permiso

class RolesPermisosDAO(DataAccessDAO):
    "Permite ver los permisos de los dos roles: admin y usuario"
    @staticmethod
    def leer(id_rol: int)-> List[Permiso]:
        try:
            with get_cursor(commit=False, dictionary=True) as cursor:
                query = """
                    SELECT p.id_permiso, p.nombre 
                    FROM roles_permisos rp
                    JOIN permisos p ON p.id_permiso = rp.id_permiso
                    WHERE rp.id_rol = %s
                """
                cursor.execute(query, (id_rol,))
                rows = cursor.fetchall()
                return [Permiso(r['id_permiso'], r['nombre']) for r in rows]
        except mysql.connector.Error as e:
            logger.exception("No se pudo obtener informacion acerca de los permisos.")
            raise e