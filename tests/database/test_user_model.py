import pytest
from sqlalchemy.exc import IntegrityError
from database.models.user import User

class TestUserModel:
    """Pruebas del modelo User"""

    def test_crear_usuario_basico(self, session):
        user = User(nombre="Juan", telefono="3001234567")
        user.set_password("password123")

        session.add(user)
        session.commit()

        assert user.id is not None
        assert user.nombre == "Juan"
        assert user.conectado is False

    def test_password_hasheada(self, session):
        user = User(nombre="Juan", telefono="3001234567")
        user.set_password("password123")

        session.add(user)
        session.commit()

        assert user.password != "password123"
        assert user.check_password("password123") is True
        assert user.check_password("wrongpass") is False

    def test_telefono_unique(self, session):
        user1 = User(nombre="Juan", telefono="3001234567")
        user1.set_password("pass123")
        session.add(user1)
        session.commit()

        user2 = User(nombre="Pedro", telefono="3001234567")
        user2.set_password("pass456")
        session.add(user2)

        with pytest.raises(IntegrityError):
            session.commit()

    def test_validacion_nombre_vacio(self):
        user = User()
        with pytest.raises(ValueError) as exc_info:
            user.nombre = ""  # Esto activará el validador
        assert "El nombre no puede estar vacío" in str(exc_info.value)

    def test_validacion_nombre_demasiado_largo(self):
        user = User()
        with pytest.raises(ValueError) as exc_info:
            user.nombre = "A" * 51  # Esto activará el validador
        assert "no puede exceder 50 caracteres" in str(exc_info.value)

    def test_validacion_telefono_vacio(self):
        user = User()
        with pytest.raises(ValueError) as exc_info:
            user.telefono = ""  # Esto activará el validador
        assert "El teléfono no puede estar vacío" in str(exc_info.value)

    def test_password_minima_longitud(self):
        user = User(nombre="Juan", telefono="3001234567")

        with pytest.raises(ValueError) as exc_info:
            user.set_password("12345")
        assert "al menos 6 caracteres" in str(exc_info.value)

    def test_to_dict_no_incluye_password(self, session):
        user = User(nombre="Juan", telefono="3001234567")
        user.set_password("password123")
        session.add(user)
        session.commit()

        user_dict = user.to_dict()

        assert "password" not in user_dict
        assert "nombre" in user_dict
        assert "telefono" in user_dict
        assert user_dict["nombre"] == "Juan"
        assert user_dict["telefono"] == "3001234567"

    def test_valores_por_defecto(self, session):
        user = User(nombre="Juan", telefono="3001234567")
        user.set_password("password123")
        
        session.add(user)
        session.commit()

        # Verificar los valores por defecto - ajusta según tus constantes reales
        assert user.rol in ["USUARIO", "usuario"]  # Ajusta según tu implementación
        assert user.estado in ["ACTIVO", "activo"]  # Ajusta según tu implementación
        assert user.conectado is False
        assert user.ultima_conexion is None

    def test_crear_usuario_valido(self, session):
        """Test para crear un usuario con datos válidos"""
        user = User(nombre="Juan Pérez", telefono="3001234567")
        user.set_password("password123")
        
        session.add(user)
        session.commit()
        
        # Verificar que se creó correctamente
        user_db = session.query(User).filter_by(telefono="3001234567").first()
        assert user_db is not None
        assert user_db.nombre == "Juan Pérez"
        assert user_db.check_password("password123") is True