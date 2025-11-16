class TestAuth:

    def test_registrar_usuario_exitoso(self, client):
        response = client.post('/auth/register', json={
            "nombre": "Juan Pérez",
            "telefono": "3001234567",
            "password": "password123",
            "confirm_password": "password123"
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['nombre'] == "Juan Pérez"

    def test_registrar_usuario_passwords_no_coinciden(self, client):
        response = client.post('/auth/register', json={
            "nombre": "Juan",
            "telefono": "3001234567",
            "password": "1234",
            "confirm_password": "5678"
        })
        assert response.status_code == 422

    def test_registrar_usuario_duplicado(self, client, usuario_registrado):
        response = client.post('/auth/register', json={
            "nombre": "Pedro",
            "telefono": "3001234567",
            "password": "1234",
            "confirm_password": "1234"
        })
        assert response.status_code == 409

    def test_login_exitoso(self, client, usuario_registrado):
        response = client.post('/auth/login', json={
            "telefono": "3001234567",
            "password": "testpass123"
        })
        assert response.status_code == 200

    def test_login_password_incorrecta(self, client, usuario_registrado):
        response = client.post('/auth/login', json={
            "telefono": "3001234567",
            "password": "incorrecta"
        })
        assert response.status_code == 401

    def test_login_usuario_no_existe(self, client):
        response = client.post('/auth/login', json={
            "telefono": "99999999",
            "password": "1234"
        })
        assert response.status_code == 401
