"""
Pruebas Unitarias para utilidades de datetime
Ejecutar: pytest tests/unit/test_datetime_utils.py -v
"""
import pytest
from datetime import datetime, timezone


class TestDatetimeUtils:
    """Pruebas para utilidades de datetime"""
    
    def test_now_utc_retorna_timezone_aware(self):
        """Test: now_utc() retorna datetime con timezone"""
        from utils.datetime_utils import now_utc
        
        resultado = now_utc()
        
        assert resultado.tzinfo is not None
        assert resultado.tzinfo == timezone.utc
        
    
    def test_parse_timestamp_formato_iso(self):
        """Test: Parsear timestamp en formato ISO"""
        from utils.datetime_utils import parse_timestamp
        
        timestamp_str = "2025-11-15 19:30:00"
        resultado = parse_timestamp(timestamp_str)
        
        assert resultado.year == 2025
        assert resultado.month == 11
        assert resultado.day == 15
        assert resultado.tzinfo is not None
        assert resultado.tzinfo == timezone.utc
    
    def test_parse_timestamp_formato_invalido(self):
        """Test: Error al parsear formato inválido"""
        from utils.datetime_utils import parse_timestamp
        
        with pytest.raises(ValueError):
            parse_timestamp("fecha-invalida")
    
    def test_make_aware_convierte_naive_a_aware(self):
        """Test: Convertir datetime naive a aware"""
        from utils.datetime_utils import make_aware
        
        dt_naive = datetime(2025, 11, 15, 12, 0, 0)
        resultado = make_aware(dt_naive)
        
        assert resultado.tzinfo is not None
        assert resultado.tzinfo == timezone.utc