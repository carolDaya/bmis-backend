from flask import Blueprint, request, jsonify
from services.user_service import UserService
from exceptions.custom_exceptions import (
    ValidationException
)
import logging
from utils.validators import require_json

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
@require_json("nombre", "telefono", "password", "confirm_password")
def register():
    data = request.json
    
    if data["password"] != data["confirm_password"]:
        raise ValidationException("Las contraseñas no coinciden")
    
    user = UserService.crear_usuario(
        nombre=data["nombre"],
        telefono=data["telefono"],
        password=data["password"]
    )
    
    return jsonify({
        "message": "Usuario creado exitosamente",
        **user.to_dict()
    }), 201


@auth_bp.route("/login", methods=["POST"])
@require_json("telefono", "password")
def login():
    data = request.json
    user = UserService.login_usuario(data["telefono"], data["password"])
    
    if user.estado == "bloqueado":
        logger.warning(f"Intento de login de usuario bloqueado: {user.telefono}")
        return jsonify({
            "error": "Usuario bloqueado",
            "detalle": "Comuníquese con el administrador."
        }), 403
    
    return jsonify({
        "message": "Login exitoso",
        **user.to_dict()
    }), 200

# Verificación de teléfono para restablecimiento
@auth_bp.route("/password/reset-request", methods=["POST"])
def verificar_telefono():
    data = request.json

    if not data or "telefono" not in data:
        raise ValidationException("Debe enviar el teléfono")

    usuario = UserService.verificar_existencia_telefono(data["telefono"])

    return jsonify({
        "mensaje": "Teléfono válido. Proceda con el cambio de contraseña.",
        "telefono": usuario.telefono
    }), 200

#  Cambio de contraseña (PATCH)
@auth_bp.route("/password", methods=["PATCH"])
def cambiar_password():
    data = request.json

    required_fields = ["telefono", "nueva_contrasena", "confirmar_contrasena"]
    if not data or not all(field in data for field in required_fields):
        raise ValidationException("Debe completar todos los campos")

    if data["nueva_contrasena"] != data["confirmar_contrasena"]:
        raise ValidationException("Las contraseñas no coinciden")

    # Llamar al servicio (lanza excepciones si falla)
    UserService.restablecer_contrasena(
        data["telefono"],
        data["nueva_contrasena"]
    )

    return jsonify({"mensaje": "Contraseña actualizada correctamente"}), 200
