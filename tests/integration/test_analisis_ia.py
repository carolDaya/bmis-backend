class TestAnalisisIA:

    def test_analizar_sin_proceso(self, client):
        r = client.get('/api/analizar')
        assert r.status_code == 200
        data = r.get_json()
        assert data["alerta_ia"] == 0

    def test_analizar_con_proceso_activo(self, client, proceso_activo):
        r = client.get('/api/analizar')
        assert r.status_code == 200
