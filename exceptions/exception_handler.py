from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from .custom_exceptions import *

def register_exception_handlers(app):
    """
    Registra manejadores globales de excepciones en la aplicación Flask
    """
    
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        response = {
            "error": error.__class__.__name__,
            "message": error.message,
            "status_code": error.status_code
        }
        if error.details:
            response["details"] = error.details
        return jsonify(response), error.status_code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        # Error de integridad de BD (claves duplicadas, foreign keys, etc.)
        db_message = str(error.orig) if hasattr(error, 'orig') else str(error)
        response = {
            "error": "DatabaseIntegrityError",
            "message": "Error de integridad en la base de datos",
            "details": db_message,
            "status_code": 409
        }
        return jsonify(response), 409

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        # Error genérico de SQLAlchemy
        response = {
            "error": "DatabaseError",
            "message": "Error en la base de datos",
            "status_code": 500
        }
        # Log del error completo (en producción usar logging)
        print(f"SQLAlchemy Error: {str(error)}")
        return jsonify(response), 500

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        response = {
            "error": "ValidationError",
            "message": str(error),
            "status_code": 422
        }
        return jsonify(response), 422

    @app.errorhandler(404)
    def handle_not_found(error):
        response = {
            "error": "NotFound",
            "message": "Recurso no encontrado",
            "status_code": 404
        }
        return jsonify(response), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        response = {
            "error": "MethodNotAllowed",
            "message": "Método no permitido",
            "status_code": 405
        }
        return jsonify(response), 405

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        # Manejo de cualquier excepción no capturada
        response = {
            "error": "InternalServerError",
            "message": "Error interno del servidor",
            "status_code": 500
        }
        # Log del error completo
        print(f"Unhandled Exception: {str(error)}")
        return jsonify(response), 500