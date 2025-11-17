class AppException(Exception):
    """Excepción base de la aplicación"""
    def __init__(self, message, status_code=500, details=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details

class DatabaseException(AppException):
    """Excepciones relacionadas con la base de datos"""
    def __init__(self, message, details=None):
        super().__init__(message, 500, details)

class BusinessLogicException(AppException):
    """Excepciones de lógica de negocio"""
    def __init__(self, message, status_code=400, details=None):
        super().__init__(message, status_code, details)

class AuthenticationException(AppException):
    """Excepciones de autenticación y autorización"""
    def __init__(self, message, status_code=401, details=None):
        super().__init__(message, status_code, details)

class ValidationException(AppException):
    """Excepciones de validación de datos"""
    def __init__(self, message, status_code=422, details=None):
        super().__init__(message, status_code, details)

class ResourceNotFoundException(AppException):
    """Excepción cuando no se encuentra un recurso"""
    def __init__(self, message, status_code=404, details=None):
        super().__init__(message, status_code, details)