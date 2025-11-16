import logging
from database.models.sensor import Sensor
from database.connection import db
from exceptions.custom_exceptions import ValidationException, DatabaseException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

logger = logging.getLogger(__name__)

def crear_sensor(nombre, tipo, unidad):
    """Crea un nuevo sensor con validación y logging"""
    logger.info(f"Intentando crear sensor: {nombre}")
    
    # Validación de duplicados
    if Sensor.query.filter_by(nombre=nombre).first():
        logger.warning(f"Intento de crear sensor duplicado: {nombre}")
        raise ValidationException(
            f"Ya existe un sensor con el nombre '{nombre}'",
            status_code=409
        )
    
    sensor = Sensor(nombre=nombre, tipo=tipo, unidad=unidad)
    
    try:
        db.session.add(sensor)
        db.session.commit()
        logger.info(f"Sensor creado exitosamente: ID={sensor.id}, nombre={nombre}")
        return sensor
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Error de integridad al crear sensor: {e}")
        raise DatabaseException(
            "Error de integridad al crear el sensor",
            details=str(e.orig) if hasattr(e, 'orig') else str(e)
        )
        
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error de base de datos al crear sensor: {e}")
        raise DatabaseException(
            "Error al guardar el sensor en la base de datos",
            details=str(e)
        )
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error inesperado al crear sensor: {e}", exc_info=True)
        raise DatabaseException(f"Error inesperado: {str(e)}")


def obtener_sensores():
    """Obtiene todos los sensores con logging"""
    logger.info("Obteniendo lista de sensores")
    try:
        sensores = Sensor.query.all()
        logger.info(f"Se obtuvieron {len(sensores)} sensores")
        return sensores
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener sensores: {e}")
        raise DatabaseException("Error al obtener la lista de sensores")


def obtener_sensor_por_id(sensor_id):
    """Obtiene un sensor por ID con validación"""
    logger.info(f"Buscando sensor con ID: {sensor_id}")
    sensor = Sensor.query.get(sensor_id)
    
    if not sensor:
        logger.warning(f"Sensor no encontrado: ID={sensor_id}")
        raise ValidationException(f"Sensor con ID {sensor_id} no encontrado", status_code=404)
    
    return sensor