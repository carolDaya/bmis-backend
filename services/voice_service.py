"""
Servicio para manejar la configuración de voz
"""
import logging
from database.models.voice_config import VoiceConfig
from database.connection import db
from exceptions.custom_exceptions import ValidationException, DatabaseException
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class VoiceService:
    """Servicio para la configuración de voz"""

    @staticmethod
    def obtener_configuracion():
        """Obtiene la configuración de voz o retorna valores por defecto"""
        logger.info("Obteniendo configuración de voz")
        try:
            config = VoiceConfig.query.get(1)
            if config:
                logger.debug("Configuración de voz encontrada en BD")
                return config
            else:
                logger.debug("Usando configuración de voz por defecto")
                return VoiceConfig()  # Retorna instancia con valores por defecto
                
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener configuración de voz: {e}")
            raise DatabaseException("Error al obtener la configuración de voz")

    @staticmethod
    def guardar_configuracion(voice_gender, voice_pitch):
        """Guarda o actualiza la configuración de voz"""
        logger.info(f"Guardando configuración de voz: gender={voice_gender}, pitch={voice_pitch}")
        
        # Validaciones
        if not voice_gender or not voice_pitch:
            raise ValidationException("voice_gender y voice_pitch son obligatorios")
        
        if voice_gender not in VoiceConfig.VALID_GENDERS:
            raise ValidationException(
                f"voice_gender inválido. Valores válidos: {VoiceConfig.VALID_GENDERS}"
            )
        
        try:
            # Convertir pitch a float y validar
            pitch_float = float(voice_pitch)
            if pitch_float < 0.5 or pitch_float > 2.0:
                raise ValidationException("voice_pitch debe estar entre 0.5 y 2.0")
                
        except (ValueError, TypeError):
            raise ValidationException("voice_pitch debe ser un número válido")

        try:
            config = VoiceConfig.query.get(1)
            
            if config is None:
                # Crear nueva configuración
                config = VoiceConfig(
                    id=1, 
                    voice_gender=voice_gender, 
                    voice_pitch=pitch_float
                )
                db.session.add(config)
                logger.info("Nueva configuración de voz creada")
            else:
                # Actualizar configuración existente
                config.voice_gender = voice_gender
                config.voice_pitch = pitch_float
                logger.info("Configuración de voz actualizada")
            
            db.session.commit()
            logger.info("Configuración de voz guardada exitosamente")
            return config
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error de BD al guardar configuración de voz: {e}")
            raise DatabaseException("Error al guardar la configuración de voz")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error inesperado al guardar configuración de voz: {e}")
            raise DatabaseException("Error al guardar la configuración de voz")