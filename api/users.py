from flask import Blueprint, jsonify
from database.connection import db
from models.user import User

users_bp = Blueprint("users", __name__)

# 📍 Ruta para obtener todos los usuarios
@users_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.all()
        user_list = []
        for user in users:
            user_list.append({
                "id": user.id,
                "nombre": user.nombre,
                "telefono": user.telefono,
                "rol": user.rol,
                "estado": user.estado,
                "conectado": user.conectado,
                "ultima_conexion": (
                    user.ultima_conexion.strftime("%Y-%m-%d %H:%M:%S")
                    if user.ultima_conexion else None
                )
            })
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📍 Ruta para obtener solo los usuarios activos
@users_bp.route("/users/active", methods=["GET"])
def get_active_users():
    try:
        activos = User.query.filter_by(estado="activo").all()
        user_list = []
        for user in activos:
            user_list.append({
                "id": user.id,
                "nombre": user.nombre,
                "telefono": user.telefono,
                "rol": user.rol,
                "estado": user.estado,
                "conectado": user.conectado,
                "ultima_conexion": (
                    user.ultima_conexion.strftime("%Y-%m-%d %H:%M:%S")
                    if user.ultima_conexion else None
                )
            })
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para obtener solo los usuarios bloqueados
@users_bp.route('/users/blocked', methods=['GET'])
def get_blocked_users():
    try:
        # Filtrar usuarios donde estado = 'bloqueado'
        users = User.query.filter_by(estado='bloqueado').all()
        user_list = []

        for user in users:
            user_list.append({
                "id": user.id,
                "nombre": user.nombre,
                "telefono": user.telefono,
                "rol": user.rol,
                "estado": user.estado,
                "conectado": user.conectado,
                "ultima_conexion": (
                    user.ultima_conexion.strftime('%Y-%m-%d %H:%M:%S')
                    if user.ultima_conexion else None
                )
            })

        return jsonify(user_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
