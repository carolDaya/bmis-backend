from flask import Blueprint, request, jsonify
from services.user_service import crear_usuario, login_usuario
from models.user import User  # Importar User aquí
from database.connection import db
from datetime import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # Validar que lleguen todos los campos
    if not data or "nombre" not in data or "telefono" not in data \
       or "password" not in data or "confirm_password" not in data:
        return jsonify({"error": "Faltan datos para el registro"}), 400

    # Validar que las contraseñas coincidan
    if data["password"] != data["confirm_password"]:
        return jsonify({"error": "Las contraseñas no coinciden"}), 400


    user, error = crear_usuario(
        nombre=data["nombre"],
        telefono=data["telefono"],
        password=data["password"]
    )

    # Si hubo error al crear el usuario 
    if error:
        return jsonify({"error": error}), 400

    # Respuesta exitosa
    return jsonify({
        "message": "Usuario creado exitosamente",
        "id": user.id,
        "rol": user.rol,
        "estado": user.estado
    }), 201

# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    # Verificar si se envió teléfono y contraseña
    if not data or "telefono" not in data or "password" not in data:
        return jsonify({"error": "Usuario no registrado"}), 404

    # Verificar si el usuario existe
    user_db = User.query.filter_by(telefono=data["telefono"]).first()
    if not user_db:
        return jsonify({"error": "Usuario no registrado"}), 404

    # Verificar contraseña
    user = login_usuario(data["telefono"], data["password"])
    if user:
        return jsonify({
            "message": "Login exitoso",
            "usuario": user.nombre,
            "rol": user.rol,
            "ultima_conexion": user.ultima_conexion
        }), 200
    else:
        # Si el usuario existe pero la contraseña es incorrecta
        return jsonify({"error": "Contraseña incorrecta"}), 401
