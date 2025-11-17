# database/db_service.py
import logging
from database.models.lectura import Lectura
from database.models.proceso_biodigestor import ProcesoBiodigestor
from database.models.sensor import Sensor
from database.connection import db
from sqlalchemy import desc
from exceptions.custom_exceptions import ResourceNotFoundException

logger = logging.getLogger(__name__)

class LecturaException(Exception):
    pass


def get_sensor_id_by_name(nombre):
    """Obtiene ID de sensor por nombre"""
    sensor = Sensor.query.filter_by(nombre=nombre).first()
    if not sensor:
        logger.error(f"Sensor no encontrado: {nombre}")
        raise ResourceNotFoundException(f"Sensor '{nombre}' no encontrado")
    return sensor.id


def obtener_fecha_inicio_proceso_activo():
    """
    Retorna la fecha de inicio del proceso ACTIVO o None si no hay.
    """
    proceso = ProcesoBiodigestor.query.filter_by(estado='ACTIVO').first()
    return proceso.fecha_inicio if proceso else None


def hay_proceso_activo():
    """Verifica proceso activo con logging"""
    proceso = ProcesoBiodigestor.query.filter_by(estado='ACTIVO').first()
    
    if proceso:
        logger.debug(f"Proceso activo encontrado: ID={proceso.id}")
    else:
        logger.debug("No hay proceso activo")
    
    return proceso


def obtener_ultima_lectura_combinada():
    """Obtiene última lectura de todos los sensores del proceso activo"""
    logger.info("Obteniendo última lectura combinada")
    
    try:
        proceso_activo = hay_proceso_activo()
        if not proceso_activo:
            raise LecturaException("No hay proceso activo")
        
        proceso_id = proceso_activo.id
        
        # Obtener IDs dinámicamente
        sensor_temp_id = get_sensor_id_by_name("temperatura")
        sensor_pres_id = get_sensor_id_by_name("presion")
        sensor_gas_id = get_sensor_id_by_name("gas")
        
        # Queries individuales
        ultima_temp = Lectura.query\
            .filter_by(sensor_id=sensor_temp_id, proceso_id=proceso_id)\
            .order_by(desc(Lectura.fecha_hora)).first()
            
        ultima_pres = Lectura.query\
            .filter_by(sensor_id=sensor_pres_id, proceso_id=proceso_id)\
            .order_by(desc(Lectura.fecha_hora)).first()
            
        ultima_gas = Lectura.query\
            .filter_by(sensor_id=sensor_gas_id, proceso_id=proceso_id)\
            .order_by(desc(Lectura.fecha_hora)).first()
        
        if not all([ultima_temp, ultima_pres, ultima_gas]):
            logger.warning("Proceso activo sin lecturas completas")
            raise LecturaException("Proceso activo sin lecturas completas")
        
        temperatura = float(ultima_temp.valor)
        presion = float(ultima_pres.valor)
        gas = float(ultima_gas.valor)
        timestamp = max(
            ultima_temp.fecha_hora,
            ultima_pres.fecha_hora,
            ultima_gas.fecha_hora
        )
        
        logger.info(f"Lectura combinada obtenida: T={temperatura}, P={presion}, G={gas}")
        return (temperatura, presion, gas, timestamp.isoformat())
        
    except LecturaException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener lectura combinada: {e}", exc_info=True)
        raise LecturaException(f"Error al obtener lecturas: {str(e)}")