from __future__ import annotations
import re


def validar_email(email: str):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, email):
        raise ValueError(f"Email '{email}' inválido.")
