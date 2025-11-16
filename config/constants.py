from enum import Enum

class SensorType(Enum):
    GAS = "gas"
    TEMPERATURA = "temperatura"
    PRESION = "presion"

class ProcesoEstado(Enum):
    ACTIVO = "ACTIVO"
    FINALIZADO = "FINALIZADO"

class UserRole(Enum):
    USUARIO = "usuario"
    ADMIN = "admin"

class UserEstado(Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    BLOQUEADO = "bloqueado"

# Configuraciones
VOICE_CONFIG_ID = 1
DEFAULT_LECTURA_LIMIT = 20
MAX_LECTURAS_POR_SENSOR = 100

# Alertas IA
TEMPERATURA_MIN = 25
TEMPERATURA_MAX = 40
PRESION_MIN = 90
GAS_MAX = 700
