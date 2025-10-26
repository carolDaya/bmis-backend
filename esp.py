from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# --- CONFIGURACIÓN DE CREDENCIALES MySQL ---
MYSQL_USER = 'root'           # Tu usuario de MySQL
MYSQL_PASSWORD = 'carol' # Reemplaza con tu clave
MYSQL_HOST = '10.9.191.194'   # La IP del servidor (donde se ejecuta Flask/MySQL)
MYSQL_DB = 'ds18d20'          # El nombre de la base de datos que creaste

# --- CONFIGURACIÓN DE LA APLICACIÓN Y BASE DE DATOS ---
app = Flask(__name__)
# Formato URI para MySQL con pymysql: mysql+pymysql://user:pass@host/db_name
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- DEFINICIÓN DEL MODELO DE BASE DE DATOS ---
class Temperatura(db.Model):
    # Definición del nombre de la tabla en MySQL
    __tablename__ = 'temperaturas' 
    
    id = db.Column(db.Integer, primary_key=True)
    celsius = db.Column(db.Float, nullable=False)
    # MySQL usará su propio TIMESTAMP por defecto
    timestamp = db.Column(db.DateTime, default=datetime.utcnow) 

    def __repr__(self):
        return f"<Temperatura {self.celsius}°C en {self.timestamp}>"

# --- RUTA DE RECEPCIÓN (La que llama el ESP32) ---
# Ruta: http://10.9.191.194/DS18B20/Temp.php?celsius=XX.X
@app.route('/DS18B20/Temp.php', methods=['GET'])
def recibir_temperatura():
    temp_celsius = request.args.get('celsius')
    
    if temp_celsius is None:
        return "ERROR: Falta el parámetro 'celsius'", 400

    try:
        temp_float = float(temp_celsius)
    except ValueError:
        return "ERROR: El valor de 'celsius' no es un número", 400

    # Guardar en MySQL
    try:
        nueva_temperatura = Temperatura(celsius=temp_float)
        db.session.add(nueva_temperatura)
        db.session.commit()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] OK: Temperatura recibida y guardada: {temp_float}°C")
        
        # Respuesta que recibe el ESP32
        return "OK", 200 
        
    except Exception as e:
        db.session.rollback()
        print(f"ERROR al guardar en DB: {e}")
        return "ERROR: Fallo al guardar en base de datos", 500

# --- INICIALIZACIÓN Y EJECUCIÓN DEL SERVIDOR ---
if __name__ == '__main__':
    # Crea la tabla 'temperaturas' si no existe en la DB de MySQL
    with app.app_context():
        db.create_all()

    # Ejecuta en el host 10.9.191.194, puerto 80.
    print(f"Servidor Flask iniciado en http://{MYSQL_HOST}:80")
    app.run(host=MYSQL_HOST, port=80, debug=True)