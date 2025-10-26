from main import create_app
from database.connection import db

def create_all_tables():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("✅ Todas las tablas fueron creadas correctamente en la base de datos.")

if __name__ == "__main__":
    create_all_tables()
