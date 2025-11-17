from flask import Blueprint, jsonify, request
from services.voice_service import VoiceService
from exceptions.custom_exceptions import ValidationException, DatabaseException
import logging

logger = logging.getLogger(__name__)
voice_bp = Blueprint('voice', __name__)

@voice_bp.get('/voice')
def get_voice_config():
    """Recupera la configuración de voz guardada"""
    try:
        config = VoiceService.obtener_configuracion()
        return jsonify(config.to_dict()), 200
        
    except DatabaseException as e:
        logger.error(f"Error al obtener configuración de voz: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500

@voice_bp.post('/voice')
def save_voice_config():
    """Guarda o actualiza la configuración de voz"""
    data = request.json
    
    if not data:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400
        
    try:
        config = VoiceService.guardar_configuracion(
            voice_gender=data.get('voice_gender'),
            voice_pitch=data.get('voice_pitch')
        )
        return jsonify(config.to_dict()), 200
        
    except ValidationException as e:
        logger.warning(f"Validación fallida: {e}")
        return jsonify({"error": str(e)}), 400
    except DatabaseException as e:
        logger.error(f"Error de BD: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logger.error(f"Error inesperado: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500