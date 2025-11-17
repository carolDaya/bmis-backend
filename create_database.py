# create_database.py - VERSIÓN CORREGIDA
import sys
import os
from sqlalchemy import text  # ✅ IMPORTANTE: Agregar esta importación

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import create_app
from database.connection import db

def create_tables():
    """Crear todas las tablas en la base de datos Aiven"""
    
    # Crear la aplicación
    app = create_app()
    
    with app.app_context():
        try:
            print("🔄 Creando tablas en Aiven MySQL...")
            
            # Importar todos los modelos
            from database.models.user import User
            from database.models.sensor import Sensor
            from database.models.lectura import Lectura
            from database.models.proceso_biodigestor import ProcesoBiodigestor
            from database.models.graph_config import GraphConfig
            from database.models.voice_config import VoiceConfig
            print("✅ Todos los modelos importados correctamente")
            
            # Crear todas las tablas
            db.create_all()
            
            print("✅ ¡Todas las tablas creadas exitosamente!")
            
            # ✅ CORREGIDO: Usar text() para consultas SQL
            result = db.session.execute(text('SHOW TABLES'))
            tables = [table[0] for table in result.fetchall()]
            print("📊 Tablas en la base de datos:")
            for table in tables:
                print(f"   - {table}")
                
            # Verificar estructura de tablas importantes
            print("\n🔍 Estructura de tablas clave:")
            for table_name in ['usuarios', 'sensores', 'lecturas', 'proceso_biodigestor']:
                if table_name in tables:
                    print(f"\nEstructura de {table_name}:")
                    columns = db.session.execute(text(f'DESCRIBE {table_name}'))
                    for column in columns:
                        print(f"   - {column[0]} ({column[1]})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando tablas: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = create_tables()
    if success:
        print("\n🎉 ¡Base de datos completamente configurada!")
        print("🚀 ¡Tu backend está listo para usar!")
    else:
        print("\n💥 Error en la configuración de la base de datos")