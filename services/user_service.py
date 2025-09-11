from models.user import User
from database.connection import db
from datetime import datetime

def crear_usuario(nombre, telefono, password):
    # Verificar si ya existe un usuario con ese teléfono
    if User.query.filter_by(telefono=telefono).first():
        return None, "El teléfono ya está registrado"

    user = User(
        nombre=nombre,
        telefono=telefono,
        rol="usuario",       # siempre usuario por defecto
        estado="activo",
        conectado=False
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()
    return user, None

def login_usuario(telefono, password):
    user = User.query.filter_by(telefono=telefono).first()
    if user and user.check_password(password):
        # actualizar conexión
        user.conectado = True
        user.ultima_conexion = datetime.now()
        db.session.commit()
        return user
    return None
