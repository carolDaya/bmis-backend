import logging
import os
from flask import Flask, jsonify
from flask_cors import CORS
from database.connection import init_app
from config.logging_config import setup_logging
from exceptions.exception_handler import register_exception_handlers
from sqlalchemy import text  # ✅ AGREGADO

# Importar blueprints
from routes.auth_bp import auth_bp
from routes.sensors_bp import sensors_bp
from routes.graph_bp import graph_bp
from routes.lectura_bp import lectura_bp
from routes.ai_bp import ai_bp
from routes.users_bp import users_bp
from routes.voice_bp import voice_bp
from routes.proceso_bp import proceso_bp

def create_app():
    app = Flask(__name__)
    
    # Configurar logging PRIMERO
    logger = setup_logging(app)
    logger.info("=== Iniciando aplicación Biodigestor ===")
    
    # ✅ AGREGADO: Verificar modelos ML antes de continuar
    ML_DIR = os.path.join(os.path.dirname(__file__), 'ml')
    required_ml_files = ['modelo_alerta.pkl', 'modelo_tipo_alerta.pkl']
    
    missing_files = []
    for file in required_ml_files:
        file_path = os.path.join(ML_DIR, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"❌ FALTAN ARCHIVOS ML CRÍTICOS: {', '.join(missing_files)}")
        logger.error("❌ La aplicación NO puede iniciar sin los modelos ML")
        logger.error("❌ Ejecute el script de entrenamiento primero")
        raise RuntimeError(f"Archivos ML faltantes: {', '.join(missing_files)}")
    
    logger.info("✅ Modelos ML verificados correctamente")
    
    # Inicializar DB
    init_app(app)
    
    # CORS
    CORS(app)
    logger.info("CORS habilitado")
    
    # Registrar manejadores de excepciones
    register_exception_handlers(app)
    logger.info("Manejadores de excepciones registrados")
    
    # ✅ CORREGIDO: Health check endpoint
    @app.route('/health')
    def health_check():
        """Endpoint para verificar salud de la aplicación"""
        try:
            from database.connection import db
            from utils.datetime_utils import now_utc
            
            # ✅ FIX: Usar text() para SQL explícito
            db.session.execute(text('SELECT 1'))
            db_status = 'healthy'
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            db_status = 'unhealthy'
        
        status_code = 200 if db_status == 'healthy' else 503
        
        return jsonify({
            'status': 'ok' if db_status == 'healthy' else 'degraded',
            'database': db_status,
            'timestamp': now_utc().isoformat()  # ✅ FIX: Usar función UTC
        }), status_code
    
    # Registrar blueprints
    blueprints = [
        (auth_bp, "/auth"),
        (sensors_bp, "/api"),
        (graph_bp, "/api"),
        (ai_bp, "/api"),
        (lectura_bp, "/api"),
        (users_bp, "/api"),
        (voice_bp, "/api"),
        (proceso_bp, "/api")
    ]
    
    for blueprint, prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=prefix)
        logger.info(f"Blueprint registrado: {blueprint.name} en {prefix}")
    
    logger.info("=== Aplicación iniciada correctamente ===")
    return app


if __name__ == "__main__":
    app = create_app()
    # ✅ MODIFICADO: Advertencia si se usa en producción
    import sys
    if '--production' in sys.argv:
        print("❌ ERROR: NO usar Flask development server en producción")
        print("✅ Usar: gunicorn -c gunicorn_config.py 'main:create_app()'")
        sys.exit(1)
    
    print("⚠️  MODO DESARROLLO - No usar en producción")
    app.run(host="0.0.0.0", port=5000, debug=True)