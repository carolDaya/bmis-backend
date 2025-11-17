class TestSensores:

    def test_crear_sensor_exitoso(self, client):
        response = client.post('/api/sensores', json={
            "nombre": "humedad",
            "tipo": "humedad",
            "unidad": "%"
        })
        assert response.status_code == 201

    def test_crear_sensor_duplicado(self, client, init_sensores):
        response = client.post('/api/sensores', json={
            "nombre": "temperatura",
            "tipo": "temperatura",
            "unidad": "°C"
        })
        assert response.status_code == 409

    def test_listar_sensores(self, client, init_sensores):
        response = client.get('/api/sensores')
        assert response.status_code == 200
        assert len(response.get_json()) == 3

    def test_obtener_sensor_por_id(self, client, init_sensores):
        response = client.get('/api/sensores/1')
        assert response.status_code == 200
