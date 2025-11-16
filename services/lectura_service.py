import logging
from database.models.lectura import Lectura
from database.models.proceso_biodigestor import ProcesoBiodigestor
from database.connection import db
from datetime import datetime, timezone
from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from exceptions.custom_exceptions import ValidationException, DatabaseException
from config.constants import DEFAULT_LECTURA_LIMIT

logger = logging.getLogger(__name__)

def obtener_proceso_activo():
    """Retorna el proceso activo o None"""
    return ProcesoBiodigestor.query.filter_by(estado='ACTIVO').first()


def registrar_lectura(sensor_id, valor, observaciones=None):
    """Registra lectura con validación de proceso activo"""
    logger.info(f"Registrando lectura - Sensor: {sensor_id}, Valor: {valor}")
    
    proceso = obtener_proceso_activo()
    if not proceso:
        logger.warning("Intento de registrar lectura sin proceso activo")
        raise ValidationException(
            "No hay proceso biodigestor activo. Inicie un proceso primero.",
            status_code=409
        )
    
    lectura = Lectura(
        sensor_id=sensor_id,
        valor=valor,
        proceso_id=proceso.id,
        observaciones=observaciones,
        fecha_hora=datetime.now(timezone.utc)
    )
    
    try:
        db.session.add(lectura)
        db.session.commit()
        logger.info(f"Lectura registrada: ID={lectura.id}, Proceso={proceso.id}")
        return lectura
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al registrar lectura: {e}", exc_info=True)
        raise DatabaseException(f"Error al registrar lectura: {str(e)}")


def obtener_lecturas():
    """Retorna todas las lecturas ordenadas por fecha descendente"""
    logger.info("Obteniendo todas las lecturas")
    
    try:
        lecturas = Lectura.query.order_by(desc(Lectura.fecha_hora)).all()
        logger.info(f"Se obtuvieron {len(lecturas)} lecturas totales")
        return lecturas
        
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener lecturas: {e}")
        raise DatabaseException("Error al obtener las lecturas")


def obtener_lecturas_por_sensor(sensor_id, limite=None):
    """
    Obtiene lecturas del proceso activo con eager loading para evitar N+1
    """
    logger.info(f"Obteniendo lecturas del sensor {sensor_id}")
    
    proceso_activo = obtener_proceso_activo()
    
    if not proceso_activo:
        logger.info("No hay proceso activo, retornando lista vacía")
        return []
    
    limite = limite or DEFAULT_LECTURA_LIMIT
    
    try:
        # Usar joinedload para evitar N+1 queries
        lecturas = Lectura.query\
            .options(joinedload(Lectura.sensor))\
            .filter_by(sensor_id=sensor_id, proceso_id=proceso_activo.id)\
            .order_by(desc(Lectura.fecha_hora))\
            .limit(limite)\
            .all()
        
        logger.info(f"Se obtuvieron {len(lecturas)} lecturas del sensor {sensor_id}")
        return lecturas
        
    except SQLAlchemyError as e:
        logger.error(f"Error al obtener lecturas: {e}")
        raise DatabaseException("Error al obtener lecturas del sensor")


def eliminar_lecturas_sensor(sensor_id):
    """Elimina todas las lecturas asociadas a un sensor"""
    logger.info(f"Eliminando lecturas del sensor {sensor_id}")
    
    try:
        count = Lectura.query.filter_by(sensor_id=sensor_id).delete()
        db.session.commit()
        logger.info(f"Se eliminaron {count} lecturas del sensor {sensor_id}")
        return count
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al eliminar lecturas: {e}", exc_info=True)
        raise DatabaseException(f"Error al eliminar lecturas del sensor: {str(e)}")