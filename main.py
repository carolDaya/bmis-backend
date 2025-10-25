from flask import Flask
from database.connection import init_app, db
from api.auth import auth_bp
from api.sensor import sensors_bp
from api.users import users_bp
from services.sensor_service import crear_sensores_base, generar_datos_sinteticos

app = Flask(__name__)
init_app(app)

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(sensors_bp, url_prefix="/api")
app.register_blueprint(users_bp, url_prefix="/api") 

# Crear tablas y generar datos base
with app.app_context():
    db.create_all()
    # Crear sensores si no existen
    crear_sensores_base()
    # Generar lecturas sintéticas (30 días)
    generar_datos_sinteticos(dias=30)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
