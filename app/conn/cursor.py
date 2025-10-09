from __future__ import annotations
from contextlib import contextmanager

# Import absoluto (cuando ejecutás con: python -m app.conn.test_cursor desde /src)
try:
    from app.conn.db_conn import connect_to_mysql
except ImportError:
    # Import relativo (si corrés el archivo dentro del paquete)
    from .db_conn import connect_to_mysql

@contextmanager
def get_cursor(commit: bool = False):
    connection = connect_to_mysql()
    if connection is None:
        raise ConnectionError("No se pudo establecer conexión con la base de datos.")
    cursor = connection.cursor(dictionary=True)
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"❌ Error en transacción: {e}")
        raise
    finally:
        cursor.close()
        connection.close()
