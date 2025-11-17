class TestFlujoCompleto:

    def test_flujo_general(self, client, init_sensores):
        # 1. Iniciar proceso
        r = client.post('/api/proceso/iniciar')
        assert r.status_code == 201

        # 2. Registrar lecturas de varios sensores
        datos = [(1, 35), (2, 90), (3, 400)]
        for sid, v in datos:
            r = client.post('/api/lecturas', json={"sensor_id": sid, "valor": v})
            assert r.status_code == 201

        # 3. Consultar lecturas
        r = client.get('/api/lecturas/1')
        assert r.status_code == 200

        # 4. Finalizar
        r = client.post('/api/proceso/finalizar')
        assert r.status_code == 200
