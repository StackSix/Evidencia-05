from __future__ import annotations
from typing import Dict, Optional
import bcrypt
from app.dao.usuarios_dao import UsuarioDAO
from app.dao.domicilios_dao import DomiciliosDAO

def registrar_usuario(
        dni: int,
        id_rol: int,
        nombre: str,
        apellido: str,
        email: str,
        contrasena: str,
    ) -> int:
        if len(contrasena) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres.")

        existente = UsuarioDAO.obtener_por_email(email)
        if existente:
            raise ValueError("Ya existe un usuario con ese email.")

        # Registrar usuario
        id_usuario = UsuarioDAO.registrar_usuario(dni, id_rol, nombre, apellido, email, contrasena)
        print(f"✅ Usuario creado con ID {id_usuario}.")

        # Pedir datos de domicilio
        print("\n🏠 Registrar domicilio principal del usuario")
        direccion = input("Dirección: ").strip()
        ciudad = input("Ciudad: ").strip()
        nombre_domicilio = input("Alias del domicilio: ").strip()

        # Registrar domicilio
        id_domicilio = DomiciliosDAO.registrar_domicilio(
            direccion=direccion,
            ciudad=ciudad,
            nombre_domicilio=nombre_domicilio
        )

        # Asociar domicilio al usuario usando su DNI
        DomiciliosDAO.vincular_usuario(dni, id_domicilio)
        print(f"✅ Domicilio registrado con ID {id_domicilio}.")

        return id_usuario

def login(email: str, contrasena_plana: str) -> Optional[Dict]:
        rec = UsuarioDAO.obtener_por_email(email)
        if not rec:
            return None
        hashed = rec.pop("contrasena", None)  # viene como alias en el DAO
        if not hashed:
            return None
        ok = bcrypt.checkpw(contrasena_plana.encode("utf-8"), hashed.encode("utf-8"))
        return rec if ok else None
