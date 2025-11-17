"""
Utilidades para manejo consistente de fechas y horas
"""
from datetime import datetime, timezone

def now_utc():
    """
    Retorna timestamp UTC actual.
    Usar SIEMPRE en lugar de datetime.now()
    """
    return datetime.now(timezone.utc)

def make_aware(dt):
    """
    Convierte datetime naive a aware (UTC)
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

def parse_timestamp(timestamp_str):
    """
    Parsea string de timestamp en múltiples formatos.
    Retorna datetime aware (UTC)
    """
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%d/%m/%Y %H:%M"
    ]
    
    for fmt in formatos:
        try:
            dt = datetime.strptime(timestamp_str, fmt)
            return make_aware(dt)
        except ValueError:
            continue
    
    raise ValueError(f"Formato de timestamp no soportado: {timestamp_str}")