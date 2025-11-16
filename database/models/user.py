from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import db
from config.constants import UserRole, UserEstado
from sqlalchemy.orm import validates

class User(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), default=UserRole.USUARIO.value)
    estado = db.Column(db.String(20), default=UserEstado.ACTIVO.value)
    conectado = db.Column(db.Boolean, default=False)
    ultima_conexion = db.Column(db.DateTime, default=None)

    @validates('nombre')
    def validate_nombre(self, key, value):
        if not value or not value.strip():
            raise ValueError("El nombre no puede estar vacío")
        if len(value) > 50:
            raise ValueError("El nombre no puede exceder 50 caracteres")
        return value.strip()

    @validates('telefono')
    def validate_telefono(self, key, value):
        if not value or not value.strip():
            raise ValueError("El teléfono no puede estar vacío")
        # Opcional: agregar regex para validar formato
        return value.strip()

    def set_password(self, password):
        if len(password) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_rol(self, rol):
        valid_roles = [r.value for r in UserRole]
        if rol not in valid_roles:
            raise ValueError(f"Rol inválido. Valores válidos: {valid_roles}")
        self.rol = rol

    def set_estado(self, estado):
        valid_estados = [e.value for e in UserEstado]
        if estado not in valid_estados:
            raise ValueError(f"Estado inválido. Valores válidos: {valid_estados}")
        self.estado = estado

    def to_dict(self):
        """Serializa el usuario (sin password)"""
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "rol": self.rol,
            "estado": self.estado,
            "conectado": self.conectado,
            "ultima_conexion": (
                self.ultima_conexion.isoformat() 
                if self.ultima_conexion else None
            )
        }
