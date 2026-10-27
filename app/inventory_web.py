"""Servidor web liviano para la gestión visual de insumos."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from app.inventario import Inventario

RAIZ = Path(__file__).resolve().parent.parent


class InventoryHandler(BaseHTTPRequestHandler):
    inventario = Inventario(RAIZ / "instance" / "inventario.sqlite3") if (RAIZ / "instance").exists() else None

    def do_GET(self):
        ruta = urlparse(self.path).path
        if ruta == "/":
            return self._archivo("templates/inventario.html", "text/html; charset=utf-8")
        if ruta == "/static/inventario.js":
            return self._archivo("static/inventario.js", "text/javascript; charset=utf-8")
        if ruta == "/static/inventario.css":
            return self._archivo("static/inventario.css", "text/css; charset=utf-8")
        if ruta == "/api/insumos":
            return self._json([i.a_dict() for i in self.inventario.listar()])
        if ruta.startswith("/api/insumos/"):
            return self._ejecutar(lambda: self.inventario.obtener(int(ruta.rsplit("/", 1)[1])).a_dict())
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_PATCH(self):
        insumo_id = self._id_insumo()
        if insumo_id is None:
            return self.send_error(HTTPStatus.NOT_FOUND)
        datos = self._cuerpo_json()
        self._ejecutar(lambda: self.inventario.modificar(insumo_id, **datos).a_dict())

    def do_DELETE(self):
        insumo_id = self._id_insumo()
        if insumo_id is None:
            return self.send_error(HTTPStatus.NOT_FOUND)
        def borrar():
            self.inventario.borrar(insumo_id)
            return {"ok": True}
        self._ejecutar(borrar)

    def _id_insumo(self):
        partes = urlparse(self.path).path.strip("/").split("/")
        return int(partes[2]) if len(partes) == 3 and partes[:2] == ["api", "insumos"] else None

    def _cuerpo_json(self):
        largo = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(largo) or b"{}")

    def _ejecutar(self, operacion):
        try:
            self._json(operacion())
        except LookupError as error:
            self._json({"error": str(error)}, HTTPStatus.NOT_FOUND)
        except (ValueError, TypeError, json.JSONDecodeError) as error:
            self._json({"error": str(error)}, HTTPStatus.BAD_REQUEST)

    def _json(self, datos, estado=HTTPStatus.OK):
        cuerpo = json.dumps(datos, ensure_ascii=False).encode()
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def _archivo(self, ruta, tipo):
        cuerpo = (RAIZ / ruta).read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)


def ejecutar(puerto=8000, ruta_db=None):
    (RAIZ / "instance").mkdir(exist_ok=True)
    InventoryHandler.inventario = Inventario(ruta_db or RAIZ / "instance" / "inventario.sqlite3")
    ThreadingHTTPServer(("127.0.0.1", puerto), InventoryHandler).serve_forever()


if __name__ == "__main__":
    ejecutar()
