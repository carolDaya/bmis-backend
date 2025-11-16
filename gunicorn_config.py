"""
Configuración de Gunicorn para producción
Uso: gunicorn -c gunicorn_config.py "main:create_app()"
"""
import multiprocessing
import os

# Bind
bind = "0.0.0.0:5000"

# Workers
workers = multiprocessing.cpu_count() * 2 + 1  # Fórmula recomendada
worker_class = "sync"  # Usar "gevent" si tienes muchas conexiones concurrentes
worker_connections = 1000
max_requests = 1000  # Recicla workers cada 1000 requests (evita memory leaks)
max_requests_jitter = 50

# Timeouts
timeout = 30
graceful_timeout = 30
keepalive = 2

# Logging
accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "biodigestor_app"

# Server mechanics
daemon = False
pidfile = "/tmp/gunicorn_biodigestor.pid"
user = None
group = None
tmp_upload_dir = None

# Preload app (carga modelos ML una sola vez)
preload_app = True

# Hooks
def on_starting(server):
    """Se ejecuta antes de iniciar workers"""
    print("Iniciando servidor Gunicorn...")

def when_ready(server):
    """Se ejecuta cuando el servidor está listo"""
    print("Servidor Gunicorn listo para recibir conexiones")

def worker_int(worker):
    """Se ejecuta cuando un worker recibe SIGINT o SIGQUIT"""
    print(f"Worker {worker.pid} interrumpido")

def worker_abort(worker):
    """Se ejecuta cuando un worker muere abruptamente"""
    print(f"Worker {worker.pid} abortado")