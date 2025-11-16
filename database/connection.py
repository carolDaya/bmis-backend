import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

db = SQLAlchemy()

def init_app(app):
    """
    Inicializa la base de datos con la aplicación Flask.
    Usa variables de entorno para no hardcodear credenciales.
    """
    user = os.environ.get("DB_USER", "root")
    password = os.environ.get("DB_PASSWORD", "1234")
    host = os.environ.get("DB_HOST", "localhost")
    db_name = os.environ.get("DB_NAME", "biodigestor_db")

    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración de pool para evitar exhaustion
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,              # Máximo 10 conexiones simultáneas
        'pool_recycle': 3600,         # Recicla conexiones cada hora
        'pool_pre_ping': True,        # Verifica que la conexión esté viva
        'max_overflow': 5,            # Permite 5 conexiones extra en picos
        'pool_timeout': 30            # Timeout de 30s para obtener conexión
    }

    try:
        db.init_app(app)
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        raise