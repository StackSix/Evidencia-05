from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from .db_conn import connect_to_mysql


@contextmanager
def get_cursor(commit: bool = False, *, dictionary: bool = False) -> Iterator:
    connection = connect_to_mysql()
    if connection is None:
        raise ConnectionError("No se pudo establecer conexión con la base de datos.")

    cursor = connection.cursor(dictionary=dictionary)
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
