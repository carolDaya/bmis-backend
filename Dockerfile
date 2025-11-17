FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

# Exponer puerto
EXPOSE 5000

# Variable de entorno para producción
ENV FLASK_ENV=production

# Comando para ejecutar con Gunicorn (producción)
CMD ["gunicorn", "-c", "gunicorn_config.py", "main:create_app()"]