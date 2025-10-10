class ValidationError(ValueError):
    """Datos inválidos o faltantes."""

class NotFoundError(LookupError):
    """Recurso no encontrado."""

class DuplicateError(RuntimeError):
    """Entidad duplicada (violación de unicidad)."""
