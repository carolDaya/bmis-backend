import logging
from database.models.user import User
from database.connection import db
from datetime import datetime, timezone
from exceptions.custom_exceptions import (
    ValidationException, AuthenticationException,
    ResourceNotFoundException, DatabaseException
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

logger = logging.getLogger(__name__)


class UserService:

    @staticmethod
    def crear_usuario(nombre, telefono, password):
        """Crea usuario con validación completa"""
        logger.info(f"Creando usuario: {nombre}, teléfono: {telefono}")
        
        if not all([nombre, telefono, password]):
            raise ValidationException("Todos los campos son obligatorios")
        
        # Verificar duplicado
        if User.query.filter_by(telefono=telefono).first():
            logger.warning(f"Intento de registro con teléfono duplicado: {telefono}")
            raise ValidationException(
                "El teléfono ya está registrado",
                status_code=409
            )
        
        user = User(nombre=nombre, telefono=telefono, conectado=False)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            logger.info(f"Usuario creado: ID={user.id}, nombre={nombre}")
            return user
            
        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"Error de integridad al crear usuario: {e}")
            raise DatabaseException(
                "Error de integridad al guardar usuario",
                details=str(e.orig) if hasattr(e, 'orig') else str(e)
            )
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error de BD al crear usuario: {e}")
            raise DatabaseException("Error al guardar usuario", details=str(e))
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error inesperado al crear usuario: {e}", exc_info=True)
            raise DatabaseException(f"Error inesperado: {str(e)}")

    @staticmethod
    def login_usuario(telefono, password):
        """Login con logging de intentos"""
        logger.info(f"Intento de login: {telefono}")
        
        if not telefono or not password:
            raise ValidationException("Debe proporcionar teléfono y contraseña")
        
        user = User.query.filter_by(telefono=telefono).first()
        
        if not user or not user.check_password(password):
            logger.warning(f"Login fallido para: {telefono}")
            raise AuthenticationException("Credenciales incorrectas")
        
        try:
            user.conectado = True
            user.ultima_conexion = datetime.now(timezone.utc)
            db.session.commit()
            logger.info(f"Login exitoso: {user.nombre} (ID={user.id})")
            return user
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error al actualizar estado de conexión: {e}")
            raise DatabaseException("Error al actualizar estado de conexión")
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error inesperado en login: {e}", exc_info=True)
            raise DatabaseException(f"Error inesperado: {str(e)}")

    @staticmethod
    def verificar_existencia_telefono(telefono):
        """Retorna un usuario o levanta error si no existe"""
        logger.info(f"Verificando existencia de teléfono: {telefono}")
        
        if not telefono:
            raise ValidationException("Debe proporcionar un número de teléfono")
        
        user = User.query.filter_by(telefono=telefono).first()
        
        if not user:
            logger.warning(f"Teléfono no encontrado: {telefono}")
            raise ResourceNotFoundException("No se encontró un usuario con ese teléfono")
        
        logger.info(f"Teléfono encontrado: {telefono} - Usuario: {user.nombre}")
        return user

    @staticmethod
    def restablecer_contrasena(telefono, nueva_contrasena):
        """Actualiza la contraseña del usuario"""
        logger.info(f"Restableciendo contraseña para: {telefono}")
        
        if not telefono or not nueva_contrasena:
            raise ValidationException("Debe proporcionar teléfono y nueva contraseña")
        
        user = User.query.filter_by(telefono=telefono).first()
        
        if not user:
            logger.warning(f"Usuario no encontrado para restablecer contraseña: {telefono}")
            raise ResourceNotFoundException("No se encontró usuario con ese teléfono")
        
        try:
            user.set_password(nueva_contrasena)
            db.session.commit()
            logger.info(f"Contraseña restablecida exitosamente para: {telefono}")
            return True
            
        except ValueError as e:
            # Captura errores de validación de contraseña (ej: muy corta)
            logger.warning(f"Validación de contraseña fallida: {e}")
            raise ValidationException(str(e))
            
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Error al actualizar contraseña: {e}")
            raise DatabaseException("Error al actualizar la contraseña", details=str(e))
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error inesperado al restablecer contraseña: {e}", exc_info=True)
            raise DatabaseException(f"Error inesperado: {str(e)}")