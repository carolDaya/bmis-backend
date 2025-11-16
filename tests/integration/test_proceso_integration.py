class TestProceso:

    def test_iniciar_proceso(self, client):
        r = client.post('/api/proceso/iniciar')
        assert r.status_code == 201

    def test_iniciar_proceso_ya_activo(self, client, proceso_activo):
        r = client.post('/api/proceso/iniciar')
        assert r.status_code == 400

    def test_estado_con_proceso_activo(self, client, proceso_activo):
        r = client.get('/api/proceso/estado')
        assert r.status_code == 200
        assert r.get_json()['proceso_activo'] is True

    def test_estado_sin_proceso(self, client):
        r = client.get('/api/proceso/estado')
        assert r.status_code == 200
        assert r.get_json()['proceso_activo'] is False

    def test_finalizar_proceso_exitoso(self, client, proceso_activo):
        r = client.post('/api/proceso/finalizar')
        assert r.status_code == 200

    def test_finalizar_sin_proceso(self, client):
        r = client.post('/api/proceso/finalizar')
        assert r.status_code == 400
