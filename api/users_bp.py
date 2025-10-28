from flask import Blueprint, jsonify, request
from database.connection import db
from database.models.user import User

users_bp = Blueprint("users", __name__)

def serialize_user(user):
    """Convierte un objeto User en un diccionario JSON"""
    return {
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
    }


# 📍 Ruta para obtener todos los usuarios (excepto admin)
@users_bp.route("/users", methods=["GET"])
def get_users():
    try:
        users = User.query.filter(User.rol != "admin").all()  # 🚫 Excluye admin
        return jsonify([serialize_user(user) for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📍 Ruta para obtener solo los usuarios activos (excepto admin)
@users_bp.route("/users/active", methods=["GET"])
def get_active_users():
    try:
        activos = User.query.filter_by(estado="activo").filter(User.rol != "admin").all()  # 🚫 Excluye admin
        return jsonify([serialize_user(user) for user in activos]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📍 Ruta para obtener solo los usuarios bloqueados (excepto admin)
@users_bp.route('/users/blocked', methods=['GET'])
def get_blocked_users():
    try:
        users = User.query.filter_by(estado='bloqueado').filter(User.rol != "admin").all()  # 🚫 Excluye admin
        return jsonify([serialize_user(user) for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 📍 Ruta para actualizar el estado de un usuario (bloquear / activar)
@users_bp.route('/users/<int:user_id>/estado', methods=['PUT'])
def update_user_state(user_id):
    try:
        data = request.get_json()
        nuevo_estado = data.get('estado')

        if nuevo_estado not in ['activo', 'bloqueado']:
            return jsonify({"error": "Estado no válido. Usa 'activo' o 'bloqueado'."}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Usuario no encontrado."}), 404

        if user.rol == "admin":
            return jsonify({"error": "No se puede cambiar el estado de un usuario administrador."}), 403  # 🚫 Protección extra

        user.estado = nuevo_estado
        db.session.commit()

        return jsonify({
            "message": f"Estado del usuario {user.nombre} actualizado a '{nuevo_estado}' correctamente.",
            "user": serialize_user(user)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
