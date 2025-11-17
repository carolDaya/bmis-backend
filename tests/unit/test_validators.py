"""
Pruebas Unitarias para validadores
Ejecutar: pytest tests/unit/test_validators.py -v
"""
import pytest
from utils.validators import validate_positive_number
from exceptions.custom_exceptions import ValidationException


class TestValidators:
    """Pruebas para validadores"""
    
    def test_validate_positive_number_valido(self):
        """Test: Validar número positivo válido"""
        resultado = validate_positive_number(10.5, "temperatura")
        
        assert resultado == 10.5
    
    def test_validate_positive_number_cero(self):
        """Test: Validar que el cero es aceptado como positivo o no negativo"""
        resultado = validate_positive_number(0, "temperatura")
        
        assert resultado == 0
    
    def test_validate_positive_number_negativo(self):
        """Test: Error con número negativo"""
        with pytest.raises(ValidationException) as exc_info:
            validate_positive_number(-5, "temperatura")
        
        # CORREGIDO: Mensaje actualizado para coincidir con el validador real
        assert "debe ser un número positivo" in str(exc_info.value.message)
    
    def test_validate_positive_number_string_invalido(self):
        """Test: Error con string no numérico"""
        with pytest.raises(ValidationException) as exc_info:
            validate_positive_number("abc", "temperatura")
            
        assert "debe ser un número" in str(exc_info.value.message)
    
    def test_validate_positive_number_none(self):
        """Test: Error con valor None"""
        with pytest.raises(ValidationException) as exc_info:
            validate_positive_number(None, "temperatura")
            
        assert "debe ser un número" in str(exc_info.value.message)
    
    def test_validate_positive_number_lista(self):
        """Test: Error con lista"""
        with pytest.raises(ValidationException) as exc_info:
            validate_positive_number([1, 2, 3], "temperatura")
            
        assert "debe ser un número" in str(exc_info.value.message)