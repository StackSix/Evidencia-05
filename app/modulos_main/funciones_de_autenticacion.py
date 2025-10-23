from __future__ import annotations
from typing import Dict, Optional
import bcrypt
import re
from dao.usuarios_dao import UsuarioDAO
from dao.domicilios_dao import DomiciliosDAO


def validar_email(email: str):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        raise ValueError(f"Email '{email}' inválido.")

def registrar_usuario(
    dni: int,
    nombre: str,
    apellido: str,
    email: str,
    contrasena: str,
    rol: str = "Usuario"  
) -> int:
    if len(contrasena) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres.")
    
    validar_email(email)

    # Verificar si el email ya existe
    existente = UsuarioDAO.obtener_por_email(email)
    if existente:
        raise ValueError("Ya existe un usuario con ese email.")

    # Registrar usuario en la BD
    id_usuario = UsuarioDAO.registrar_usuario(dni, nombre, apellido, email, contrasena, rol)
    print(f"✅ Usuario creado con ID {id_usuario}.")


def login(email: str, contrasena_plana: str) -> Optional[Dict]:
        rec = UsuarioDAO.obtener_por_email(email)
        if not rec:
            return None
        hashed = rec.pop("contrasena", None)  # viene como alias en el DAO
        if not hashed:
            return None
        ok = bcrypt.checkpw(contrasena_plana.encode("utf-8"), hashed.encode("utf-8"))
        return rec if ok else None
