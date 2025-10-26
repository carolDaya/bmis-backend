from flask import Blueprint, request, jsonify
from services.user_service import (
    crear_usuario, 
    login_usuario, 
    verificar_existencia_telefono, 
    restablecer_contrasena
)

# Importaciones de la base de datos y modelos (asumiendo que están disponibles)
from database.models.user import User 
from database.connection import db 
from datetime import datetime 

auth_bp = Blueprint("auth", __name__)

# -----------------------------------------------------------------
# 1. Registro de Usuario (RESTful: Creación de recurso Usuario)
# Ruta: /register
# Método: POST
# -----------------------------------------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json

    # Validaciones en la capa de la ruta
    if not data or "nombre" not in data or "telefono" not in data \
       or "password" not in data or "confirm_password" not in data:
        return jsonify({"error": "Faltan datos para el registro"}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"error": "Las contraseñas no coinciden"}), 400

    # Llamada al servicio
    try:
        user, error = crear_usuario(
            nombre=data["nombre"],
            telefono=data["telefono"],
            password=data["password"]
        )
        
        if error:
            # Error de lógica de negocio (ej. teléfono ya registrado)
            return jsonify({"error": error}), 400

        # Respuesta exitosa: 201 Created
        return jsonify({
            "message": "Usuario creado exitosamente",
            "id": user.id,
            "rol": user.rol,
            "estado": user.estado
        }), 201
    except Exception as e:
        # Error interno del servidor
        return jsonify({"error": "Error interno al crear usuario"}), 500

# -----------------------------------------------------------------
# 2. Login de Usuario (RESTful: Creación de una Sesión)
# Ruta: /login
# Método: POST
# -----------------------------------------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data or "telefono" not in data or "password" not in data:
        return jsonify({"error": "Debe ingresar teléfono y contraseña"}), 400

    # Llamada al servicio
    user = login_usuario(data["telefono"], data["password"])
    
    if user:
        # 200 OK
        return jsonify({
            "message": "Login exitoso",
            "usuario": user.nombre,
            "rol": user.rol,
            "ultima_conexion": user.ultima_conexion
        }), 200
    else:
        # Error 401 Unauthorized (credenciales inválidas) o 404
        return jsonify({"error": "Teléfono o contraseña incorrecta"}), 401

# -----------------------------------------------------------------
# 3. Paso 1: Solicitud de Restablecimiento (Verificación)
# (RESTful: Creación de un Recurso de Solicitud de Restablecimiento)
# Ruta: /password/reset-request
# Método: POST
# -----------------------------------------------------------------
@auth_bp.route('/password/reset-request', methods=['POST'])
def verificar_telefono_ruta():
    data = request.get_json()
    telefono = data.get('telefono')

    if not telefono:
        return jsonify({"error": "Debe ingresar el número de teléfono"}), 400

    # Llamada al servicio
    usuario = verificar_existencia_telefono(telefono)

    if usuario:
        # Se asume que aquí se podría enviar un código de verificación (no implementado)
        return jsonify({"mensaje": "Teléfono válido. Procede con el cambio de contraseña.", "telefono": telefono}), 200
    else:
        # 404 Not Found
        return jsonify({"error": "No existe un usuario con ese número"}), 404

# -----------------------------------------------------------------
# 4. Paso 2: Cambio de Contraseña 
# (RESTful: Actualización Parcial del Recurso /password del usuario)
# Ruta: /password
# Método: PATCH
# -----------------------------------------------------------------
@auth_bp.route('/password', methods=['PATCH']) # <- Uso de PATCH para actualización parcial
def cambiar_contrasena_ruta():
    data = request.get_json()
    telefono = data.get('telefono')
    nueva_contrasena = data.get('nueva_contrasena')
    confirmar_contrasena = data.get('confirmar_contrasena')

    if not telefono or not nueva_contrasena or not confirmar_contrasena:
        return jsonify({"error": "Debe completar todos los campos"}), 400

    if nueva_contrasena != confirmar_contrasena:
        return jsonify({"error": "Las contraseñas no coinciden"}), 400

    # Llamada al servicio
    try:
        exito, error = restablecer_contrasena(telefono, nueva_contrasena)
        
        if error:
            # Manejar errores como "usuario no encontrado" o fallos en DB
            return jsonify({"error": error}), 404 # 404 para usuario no encontrado

        # 200 OK para una actualización exitosa con PATCH
        return jsonify({"mensaje": "Contraseña actualizada correctamente"}), 200
    except Exception as e:
        return jsonify({"error": "Error interno al actualizar la contraseña"}), 500