from flask import Flask
from flask_cors import CORS
from database.connection import init_app
from api.auth_bp import auth_bp
from api.sensors_bp import sensors_bp
from api.graph_bp import graph_bp
from api.lectura_bp import lectura_bp
from api.ai_bp import ai_bp
from api.users_bp import users_bp

def create_app():
    app = Flask(__name__)
    init_app(app)

    # Habilitar CORS para todas las rutas y orígenes
    CORS(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(sensors_bp, url_prefix="/api")
    app.register_blueprint(graph_bp, url_prefix="/api")
    app.register_blueprint(ai_bp, url_prefix="/api")
    app.register_blueprint(lectura_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api") 

    return app

# Punto de entrada principal
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
