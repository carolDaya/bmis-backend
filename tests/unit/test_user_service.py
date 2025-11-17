"""
Pruebas Unitarias para UserService
Ejecutar: pytest tests/unit/test_user_service.py -v
"""
import pytest
from unittest.mock import Mock, patch
from services.user_service import UserService
from exceptions.custom_exceptions import ValidationException, AuthenticationException, ResourceNotFoundException


class TestUserService:
    """Pruebas para UserService"""
    
    @patch('services.user_service.User')
    @patch('services.user_service.db.session')
    def test_crear_usuario_exitoso(self, mock_session, MockUser, mock_db_session):
        """Test: Crear usuario con datos válidos"""
        # Configurar mocks
        mock_user_instance = Mock()
        mock_user_instance.id = 1
        mock_user_instance.nombre = "Juan"
        MockUser.return_value = mock_user_instance
        MockUser.query.filter_by.return_value.first.return_value = None
        
        # Ejecutar
        user = UserService.crear_usuario("Juan", "3001234567", "password123")
        
        # Verificar
        assert user is not None
        assert user.nombre == "Juan"
        mock_session.add.assert_called_once_with(mock_user_instance)
        mock_session.commit.assert_called_once()
    
    @patch('services.user_service.User')
    def test_crear_usuario_telefono_duplicado(self, MockUser):
        """Test: Error al crear usuario con teléfono duplicado"""
        # Simular que ya existe un usuario con ese teléfono
        MockUser.query.filter_by.return_value.first.return_value = Mock()
        
        with pytest.raises(ValidationException) as exc_info:
            UserService.crear_usuario("Pedro", "3001234567", "password123")
        
        assert "teléfono ya está registrado" in str(exc_info.value.message)
    
    def test_crear_usuario_campos_vacios_o_nulos(self):
        """Test: Error al crear usuario con campos vacíos o nulos"""
        with patch('services.user_service.User'):
            # Caso 1: Nombre vacío
            with pytest.raises(ValidationException) as exc_info:
                UserService.crear_usuario("", "3001234567", "password123")
            assert "obligatorios" in str(exc_info.value.message)
            
            # Caso 2: Contraseña nula
            with pytest.raises(ValidationException) as exc_info:
                UserService.crear_usuario("Nombre", "3001234567", None)
            assert "obligatorios" in str(exc_info.value.message)

    @patch('services.user_service.User')
    @patch('services.user_service.db.session')
    def test_login_exitoso(self, mock_session, MockUser, mock_user):
        """Test: Login con credenciales correctas"""
        # Configurar mock para que retorne nuestro usuario mock
        MockUser.query.filter_by.return_value.first.return_value = mock_user
        
        # Ejecutar
        user = UserService.login_usuario("3001234567", "password123")
        
        # Verificar
        assert user is not None
        # Verificar que se actualizaron los campos de conexión
        assert mock_user.conectado == True
        mock_user.check_password.assert_called_once_with("password123")
        mock_session.commit.assert_called_once()
    
    @patch('services.user_service.User')
    def test_login_credenciales_incorrectas(self, MockUser):
        """Test: Login con contraseña incorrecta"""
        # Configurar mock de usuario con contraseña incorrecta
        mock_user = Mock()
        mock_user.check_password.return_value = False
        MockUser.query.filter_by.return_value.first.return_value = mock_user
        
        with pytest.raises(AuthenticationException) as exc_info:
            UserService.login_usuario("3001234567", "wrongpassword")
        
        assert "Credenciales incorrectas" in str(exc_info.value.message)
    
    @patch('services.user_service.User')
    def test_login_usuario_no_existe(self, MockUser):
        """Test: Login con teléfono que no existe"""
        # Simular que no se encuentra usuario
        MockUser.query.filter_by.return_value.first.return_value = None
        
        with pytest.raises(AuthenticationException) as exc_info:
            UserService.login_usuario("9999999999", "password123")
            
        assert "Credenciales incorrectas" in str(exc_info.value.message)
    
    @patch('services.user_service.User')
    @patch('services.user_service.db.session')
    def test_restablecer_contrasena_exitoso(self, mock_session, MockUser, mock_user):
        """Test: Restablecer contraseña correctamente"""
        # Configurar mock
        MockUser.query.filter_by.return_value.first.return_value = mock_user
        
        # Ejecutar
        result = UserService.restablecer_contrasena("3001234567", "newpass123")
        
        # Verificar
        assert result == True
        mock_user.set_password.assert_called_once_with("newpass123")
        mock_session.commit.assert_called_once()
        
    @patch('services.user_service.User')
    def test_restablecer_contrasena_usuario_no_existe(self, MockUser):
        """Test: Error al intentar restablecer contraseña de usuario inexistente"""
        # Simular usuario no encontrado
        MockUser.query.filter_by.return_value.first.return_value = None
        
        # CORREGIDO: Cambiar ValidationException por ResourceNotFoundException
        with pytest.raises(ResourceNotFoundException) as exc_info:
            UserService.restablecer_contrasena("9999999999", "newpass123")
            
        assert "No se encontró usuario con ese teléfono" in str(exc_info.value.message)

    @patch('services.user_service.User')
    def test_verificar_existencia_telefono_exitoso(self, MockUser, mock_user):
        """Test: Verificar existencia de teléfono exitoso"""
        MockUser.query.filter_by.return_value.first.return_value = mock_user
        
        user = UserService.verificar_existencia_telefono("3001234567")
        
        assert user == mock_user

    @patch('services.user_service.User')
    def test_verificar_existencia_telefono_no_existe(self, MockUser):
        """Test: Error al verificar teléfono que no existe"""
        MockUser.query.filter_by.return_value.first.return_value = None
        
        # CORREGIDO: Cambiar ValidationException por ResourceNotFoundException
        with pytest.raises(ResourceNotFoundException) as exc_info:
            UserService.verificar_existencia_telefono("9999999999")
            
        assert "No se encontró un usuario con ese teléfono" in str(exc_info.value.message)