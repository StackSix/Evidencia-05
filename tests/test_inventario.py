import tempfile
import unittest
from pathlib import Path

from app.inventario import Inventario


class InventarioTest(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.inventario = Inventario(Path(self.temporal.name) / "test.sqlite3")
        self.insumo = self.inventario.crear(codigo="TOR-1", nombre="Tornillo", categoria="Ferretería", ubicacion="A-1", unidad="u", stock=20, minimo=5, maximo=50)

    def tearDown(self):
        self.temporal.cleanup()

    def test_modifica_campos_permitidos_y_fecha(self):
        modificado = self.inventario.modificar(self.insumo.id, categoria="Repuestos", ubicacion="B-2", minimo=10, maximo=40)
        self.assertEqual((modificado.categoria, modificado.ubicacion), ("Repuestos", "B-2"))
        self.assertEqual((modificado.minimo, modificado.maximo), (10, 40))
        self.assertTrue(modificado.actualizado_en)

    def test_borrado_es_completo_por_cascada(self):
        self.inventario.actualizar_stock(self.insumo.id, 3)
        self.inventario.borrar(self.insumo.id)
        with self.assertRaises(LookupError):
            self.inventario.obtener(self.insumo.id)
        with self.inventario.conexion() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM movimientos").fetchone()[0], 0)
            self.assertEqual(db.execute("SELECT count(*) FROM notificaciones").fetchone()[0], 0)

    def test_stock_bajo_genera_notificacion(self):
        insumo, mensaje = self.inventario.actualizar_stock(self.insumo.id, 4)
        self.assertTrue(insumo.stock_bajo)
        self.assertIn("Stock bajo", mensaje)
        with self.inventario.conexion() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM notificaciones").fetchone()[0], 1)

    def test_rechaza_umbrales_invalidos(self):
        with self.assertRaises(ValueError):
            self.inventario.modificar(self.insumo.id, minimo=50, maximo=10)


if __name__ == "__main__":
    unittest.main()
