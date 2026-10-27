"""Interfaz base opcional para DAO (se mantiene por compatibilidad)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional


class DataAccessDAO(ABC):
    @abstractmethod
    def crear(self, entidad: Any) -> Any:  # pragma: no cover - interfaz
        raise NotImplementedError

    @abstractmethod
    def leer(self, identificador: Any) -> Optional[Any]:  # pragma: no cover - interfaz
        raise NotImplementedError

    @abstractmethod
    def leer_todo(self) -> Iterable[Any]:  # pragma: no cover - interfaz
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, entidad: Any) -> None:  # pragma: no cover - interfaz
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, entidad: Any) -> None:  # pragma: no cover - interfaz
        raise NotImplementedError
