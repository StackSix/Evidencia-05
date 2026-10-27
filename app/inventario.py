"""Reglas de negocio y persistencia del inventario del pañol."""

from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


def ahora_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass(frozen=True)
class Insumo:
    id: int
    codigo: str
    nombre: str
    categoria: str
    ubicacion: str
    unidad: str
    stock: float
    minimo: float
    maximo: float
    actualizado_en: str

    @property
    def stock_bajo(self) -> bool:
        return self.stock < self.minimo

    def a_dict(self) -> dict:
        return {**asdict(self), "stock_bajo": self.stock_bajo}


class Inventario:
    CAMPOS_EDITABLES = {"categoria", "ubicacion", "minimo", "maximo"}

    def __init__(self, ruta_db: str | Path):
        self.ruta_db = str(ruta_db)
        self.inicializar()

    @contextmanager
    def conexion(self) -> Iterator[sqlite3.Connection]:
        conexion = sqlite3.connect(self.ruta_db)
        conexion.row_factory = sqlite3.Row
        conexion.execute("PRAGMA foreign_keys = ON")
        try:
            yield conexion
            conexion.commit()
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def inicializar(self) -> None:
        with self.conexion() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS insumos (
                    id INTEGER PRIMARY KEY, codigo TEXT NOT NULL UNIQUE,
                    nombre TEXT NOT NULL, categoria TEXT NOT NULL,
                    ubicacion TEXT NOT NULL, unidad TEXT NOT NULL,
                    stock REAL NOT NULL DEFAULT 0 CHECK(stock >= 0),
                    minimo REAL NOT NULL CHECK(minimo >= 0),
                    maximo REAL NOT NULL CHECK(maximo > minimo),
                    actualizado_en TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS movimientos (
                    id INTEGER PRIMARY KEY, insumo_id INTEGER NOT NULL,
                    cantidad REAL NOT NULL, creado_en TEXT NOT NULL,
                    FOREIGN KEY(insumo_id) REFERENCES insumos(id) ON DELETE CASCADE
                );
                CREATE TABLE IF NOT EXISTS notificaciones (
                    id INTEGER PRIMARY KEY, insumo_id INTEGER NOT NULL,
                    mensaje TEXT NOT NULL, creado_en TEXT NOT NULL,
                    FOREIGN KEY(insumo_id) REFERENCES insumos(id) ON DELETE CASCADE
                );
                """
            )

    def listar(self) -> list[Insumo]:
        with self.conexion() as db:
            filas = db.execute("SELECT * FROM insumos ORDER BY nombre COLLATE NOCASE").fetchall()
        return [Insumo(**dict(fila)) for fila in filas]

    def obtener(self, insumo_id: int) -> Insumo:
        with self.conexion() as db:
            fila = db.execute("SELECT * FROM insumos WHERE id = ?", (insumo_id,)).fetchone()
        if fila is None:
            raise LookupError("El insumo no existe")
        return Insumo(**dict(fila))

    def crear(self, **datos) -> Insumo:
        minimo, maximo = self._umbrales(datos["minimo"], datos["maximo"])
        fecha = ahora_iso()
        with self.conexion() as db:
            cursor = db.execute(
                """INSERT INTO insumos
                   (codigo,nombre,categoria,ubicacion,unidad,stock,minimo,maximo,actualizado_en)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (datos["codigo"], datos["nombre"], datos["categoria"], datos["ubicacion"],
                 datos.get("unidad", "u"), float(datos.get("stock", 0)), minimo, maximo, fecha),
            )
            insumo_id = cursor.lastrowid
        return self.obtener(insumo_id)

    def modificar(self, insumo_id: int, **cambios) -> Insumo:
        desconocidos = set(cambios) - self.CAMPOS_EDITABLES
        if desconocidos:
            raise ValueError("Solo se pueden modificar categoría, ubicación, mínimo y máximo")
        actual = self.obtener(insumo_id)
        minimo, maximo = self._umbrales(
            cambios.get("minimo", actual.minimo), cambios.get("maximo", actual.maximo)
        )
        valores = {
            "categoria": cambios.get("categoria", actual.categoria).strip(),
            "ubicacion": cambios.get("ubicacion", actual.ubicacion).strip(),
            "minimo": minimo, "maximo": maximo,
        }
        if not valores["categoria"] or not valores["ubicacion"]:
            raise ValueError("Categoría y ubicación son obligatorias")
        with self.conexion() as db:
            db.execute(
                """UPDATE insumos SET categoria=?, ubicacion=?, minimo=?, maximo=?, actualizado_en=?
                   WHERE id=?""",
                (*valores.values(), ahora_iso(), insumo_id),
            )
        return self.obtener(insumo_id)

    def borrar(self, insumo_id: int) -> None:
        with self.conexion() as db:
            cursor = db.execute("DELETE FROM insumos WHERE id = ?", (insumo_id,))
            if cursor.rowcount != 1:
                raise LookupError("El insumo no existe")

    def actualizar_stock(self, insumo_id: int, stock: float) -> tuple[Insumo, str | None]:
        stock = float(stock)
        if stock < 0:
            raise ValueError("El stock no puede ser negativo")
        fecha = ahora_iso()
        with self.conexion() as db:
            actual = db.execute("SELECT stock FROM insumos WHERE id=?", (insumo_id,)).fetchone()
            if actual is None:
                raise LookupError("El insumo no existe")
            db.execute("UPDATE insumos SET stock=?, actualizado_en=? WHERE id=?", (stock, fecha, insumo_id))
            db.execute("INSERT INTO movimientos(insumo_id,cantidad,creado_en) VALUES(?,?,?)",
                       (insumo_id, stock - actual["stock"], fecha))
        insumo = self.obtener(insumo_id)
        mensaje = None
        if insumo.stock_bajo:
            mensaje = f"Stock bajo: {insumo.nombre} tiene {insumo.stock:g} {insumo.unidad} (mínimo {insumo.minimo:g})."
            with self.conexion() as db:
                db.execute("INSERT INTO notificaciones(insumo_id,mensaje,creado_en) VALUES(?,?,?)",
                           (insumo_id, mensaje, fecha))
        return insumo, mensaje

    @staticmethod
    def _umbrales(minimo, maximo) -> tuple[float, float]:
        minimo, maximo = float(minimo), float(maximo)
        if minimo < 0 or maximo <= minimo:
            raise ValueError("El mínimo debe ser no negativo y menor que el máximo")
        return minimo, maximo
