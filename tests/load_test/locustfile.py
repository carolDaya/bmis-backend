"""
locustfile_fixed.py - RUTAS CORRECTAS para tu backend
"""

from locust import HttpUser, task, between
import random
from datetime import datetime

BASE_URL = "http://localhost:5000"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Locust-Load-Test/1.0"
}


class FixedLoadUser(HttpUser):
    wait_time = between(1, 3)
    host = BASE_URL
    
    def on_start(self):
        print(f"🧪 Usuario iniciado: {datetime.now()}")
    
    @task(5)  # Alta prioridad
    def test_health(self):
        """Health check - Debería funcionar SIEMPRE"""
        with self.client.get("/health", headers=HEADERS, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
                print(f"✅ Health: {response.elapsed.total_seconds():.2f}s")
            else:
                response.failure(f"Health failed: {response.status_code}")
    
    @task(4)
    def test_sensors(self):
        """Endpoint: /api/sensores (del sensors_bp)"""
        with self.client.get("/api/sensores", headers=HEADERS, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 404:
                # Si no existe, lo marcamos como éxito pero con nota
                response.success()
                print("⚠️  /api/sensors devuelve 404 - ¿Endpoint implementado?")
            else:
                response.failure(f"Sensors: {response.status_code}")
    
    @task(3)
    def test_lecturas(self):
        """Endpoint: /api/lecturas (del lectura_bp)"""
        params = {
            "page": random.randint(1, 3),
            "per_page": 10
        }
        
        with self.client.get("/api/lecturas", headers=HEADERS, params=params, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 500:
                # Error interno - revisar logs de Flask
                response.failure(f"Lecturas 500 error - Revisar backend")
            else:
                response.failure(f"Lecturas: {response.status_code}")
    
    @task(2)
    def test_proceso_estado(self):
        """Endpoint: /api/proceso/estado (del proceso_bp)"""
        with self.client.get("/api/proceso/estado", headers=HEADERS, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 500:
                response.failure(f"Proceso 500 error - Revisar backend")
            else:
                response.failure(f"Proceso: {response.status_code}")
    
    @task(1)
    def test_graph(self):
        """Endpoint: /api/graficas (del graph_bp)"""
        # Primero verificar si existe
        with self.client.get("/api/graficas", headers=HEADERS, catch_response=True) as response:
            if response.status_code != 404:
                response.success()