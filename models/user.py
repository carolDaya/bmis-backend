from database.connection import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default="usuario")  # por defecto "usuario"
    estado = db.Column(db.String(20), default="activo") # manejar "activo/inactivo"
    conectado = db.Column(db.Boolean, default=False)
    ultima_conexion = db.Column(db.DateTime, default=None)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
