class TestLecturas:

    def test_registrar_lectura_exitosa(self, client, init_sensores, proceso_activo):
        r = client.post('/api/lecturas', json={
            "sensor_id": 1,
            "valor": 35.5
        })
        assert r.status_code == 201

    def test_registrar_lectura_sin_proceso(self, client, init_sensores):
        r = client.post('/api/lecturas', json={
            "sensor_id": 1,
            "valor": 50
        })
        assert r.status_code == 409

    def test_listado_paginado(self, client, init_sensores, proceso_activo):
        for i in range(15):
            client.post('/api/lecturas', json={"sensor_id": 1, "valor": i})

        r = client.get('/api/lecturas?page=1&per_page=10')
        data = r.get_json()

        assert r.status_code == 200
        assert len(data["lecturas"]) == 10

    def test_lecturas_por_sensor(self, client, init_sensores, proceso_activo):
        for i in range(5):
            client.post('/api/lecturas', json={"sensor_id": 1, "valor": i})

        r = client.get('/api/lecturas/1')
        assert r.status_code == 200
        assert len(r.get_json()) == 5
