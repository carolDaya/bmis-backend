# database/connection.py - CONFIGURACIÓN COMPLETA
import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import tempfile

load_dotenv()

db = SQLAlchemy()

def init_app(app):
    """
    Inicializa la base de datos con Aiven MySQL.
    """
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")

    # ✅ Crear archivo temporal con el certificado SSL
    ssl_cert_content = """-----BEGIN CERTIFICATE-----
MIIEUDCCArigAwIBAgIUUwj0YP3AzLaNJu4prTkM8vAtq9wwDQYJKoZIhvcNAQEM
BQAwQDE+MDwGA1UEAww1ZjBiYjEwYTQtZjk4NS00NTc1LWIxYTAtNjIzYTNhY2Mx
MzgwIEdFTiAxIFByb2plY3QgQ0EwHhcNMjUxMTE3MTQzMzUyWhcNMzUxMTE1MTQz
MzUyWjBAMT4wPAYDVQQDDDVmMGJiMTBhNC1mOTg1LTQ1NzUtYjFhMC02MjNhM2Fj
YzEzODAgR0VOIDEgUHJvamVjdCBDQTCCAaIwDQYJKoZIhvcNAQEBBQADggGPADCC
AYoCggGBAJKFICYOAFqAp5dA6ywSJ1YKPrR+Mpiz6K6d8/RDuLjAMKGCHCjuaiHO
q1bIUzB6UzlesJUnGEePxc9LY+p4ftG45dOBmBsguS4bobOeGtMKdMgJzqML5xQZ
mP6nq1TVKO2HZCEA0hrus/KKyGA9NMyz0zoy7PlBwED1YndHWad3hI1OG0O4GW1Q
0h37/Bq+ZoZKGtcd6ietpW6Tdv3z3GNkA1wfIKzPjE+6uZM8DUVhWAvpIj6cI8up
eQGbu/tWGwNKBH/BHkItfGNW5YTGE15NWu9ckiX2NO1LrTkiiWRy5+yLNbVBVFq9
lKByPI/phIeknyQr2hcUTSYQcDOg/PzAHcZ8E4cn11EUZqLpZdbFUIrQd/ReHeiD
4Mxq6+eRc6XL3/svZDVP91LLcL9ROMS/OpYOFZoOReBypANBLbk1+OkOjW1OLpC4
ta8pnyLEBfuA9zqfFo+nJU0GXMNNXBQkpgGR6jIsh8vvqPXm82Mtuu6Yly8Ifosy
6sMDuUTu3wIDAQABo0IwQDAdBgNVHQ4EFgQUhfftFXlQRKBxfjV+GNLNsNMUVEEw
EgYDVR0TAQH/BAgwBgEB/wIBADALBgNVHQ8EBAMCAQYwDQYJKoZIhvcNAQEMBQAD
ggGBABnOg6uoqwdCtq2G95YV1uRcbi0cm07vIJbI5P95Mr6nxXty92lSAz2rFTHS
DNGwLJl5XassDyWVdd+aJ9nb+vm5VgXS6UBEoQiNpMS+F6/cA86yemyHd7tqE4hA
5Kvj17DIH9GfkUcWN2Qy1MsgZUNQAdV20iWaJ7WK2gw63QbpKTh6Ij4Cvl1Ngetw
IM1AqXOHpvCPcfZaTC4EVBkoRsuCF7E0odn+Dglv2QzIdWtVB7WpdCoLIr4FmhGp
NFSLr+9nru806jcL7jb4sKNDS0Lqgr1XfFmI2KeaTBvPvDzzfQfIXM6F3LFaywaB
uRMCZaHnj18brdLb787jwsrqwcfCgUTVXNFcJD2POJ9VhhIczVDmNrUKiC87XkJ7
DXF8DzgZvDmN8Poyu+y8zpVIkp3PwVtjm30to7jt2xNlsArb2d4QoUDFSb7oLrSL
/HiPd3U9o7QRE0kuxzgALHrDu9A+BLzPyLI0qnI9JfL+WHpxj7NZB33mhm4p+ZAw
eYXSuA==
-----END CERTIFICATE-----"""

    # Crear archivo temporal para el certificado
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as cert_file:
        cert_file.write(ssl_cert_content)
        ssl_ca_path = cert_file.name

    # URI de conexión con SSL
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Configuración con SSL explícito
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 5,
        'pool_recycle': 300,
        'pool_pre_ping': True,
        'max_overflow': 2,
        'pool_timeout': 30,
        'connect_args': {
            'ssl': {
                'ca': ssl_ca_path,
                'ssl_disabled': False,
                'verify_ssl': True
            }
        }
    }

    try:
        db.init_app(app)
        print("✅ Conectado a Aiven MySQL correctamente!")
        
        # Limpiar archivo temporal después de usar
        import atexit
        atexit.register(lambda: os.unlink(ssl_ca_path) if os.path.exists(ssl_ca_path) else None)
        
    except Exception as e:
        print(f"❌ Error al conectar con Aiven: {e}")
        raise