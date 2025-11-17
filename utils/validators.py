from functools import wraps
from flask import request
from exceptions.custom_exceptions import ValidationException

def require_json(*required_fields):
    """
    Decorator para validar que el request tenga JSON y campos obligatorios
    
    Uso:
        @require_json('nombre', 'telefono', 'password')
        def register():
            data = request.json
            # data ya está validado
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                raise ValidationException("El request debe ser JSON")
            
            data = request.json
            if not data:
                raise ValidationException("El cuerpo JSON no puede estar vacío")
            
            missing = [field for field in required_fields if field not in data]
            if missing:
                raise ValidationException(
                    f"Campos obligatorios faltantes: {', '.join(missing)}"
                )
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def validate_positive_number(value, field_name):
    """Valida que un valor sea numérico positivo"""
    try:
        num = float(value)
        if num < 0:
            raise ValidationException(f"{field_name} debe ser un número positivo")
        return num
    except (ValueError, TypeError):
        raise ValidationException(f"{field_name} debe ser un número válido")