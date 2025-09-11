from database.connection import db

class Sensor(db.Model):
    __tablename__ = "sensores"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    tipo = db.Column(db.String(100), nullable=False)
    unidad = db.Column(db.String(20), nullable=False)
    activo = db.Column(db.Boolean, default=True)
