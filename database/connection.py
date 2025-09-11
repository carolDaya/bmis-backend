from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    # Configuración de conexión MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:carol@localhost/biodigestor_db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

