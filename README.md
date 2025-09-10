Proyecto Backend – Biodigestor Inteligente
📂 Estructura de Carpetas
backend/
│── venv/               # Entorno virtual (NO modificar, solo dependencias instaladas)
│── main.py              # Punto de entrada (inicia el servidor)
│── requirements.txt     # Librerías necesarias (FastAPI, scikit-learn, SQLAlchemy, etc.)
│
├── api/                 # Rutas/Endpoints
│   ├── auth.py          # Login, registro, eliminar cuenta, restablecer contraseña
│   ├── users.py         # Gestión de usuarios (listar, bloquear/desbloquear, ver activos)
│   ├── sensors.py       # Lecturas de sensores (temperatura, pH, biogás)
│   └── ai.py            # Endpoint para enviar datos y recibir predicción IA
│
├── models/              # Modelos de la base de datos
│   ├── user.py
│   ├── sensor.py
│   └── config.py        # Configuración de conexión a MySQL
│
├── services/            # Lógica de negocio
│   ├── ai_service.py    # Cargar modelo scikit-learn, predecir estado
│   ├── user_service.py  # Crear, actualizar, bloquear usuarios
│   └── sensor_service.py# Simulación y manejo de lecturas de sensores
│
├── database/            # Conexión a MySQL
│   └── connection.py
│
├── ml/                  # Inteligencia artificial
│   ├── train_model.py   # Entrenamiento con datos históricos
│   ├── synthetic_data.py# Generación de datos sintéticos para pruebas
│   ├── datasets/        # Carpeta para almacenar datasets simulados o de Kaggle
│   │   └── sensors.csv
│   └── model.pkl        # Modelo entrenado guardado
│
└── tests/               # Pruebas con Postman o PyTest
    └── test_api.py

📖 1. Visión General del Proyecto

Este proyecto busca desarrollar una aplicación móvil nativa en Android (Kotlin + Android Studio) conectada a un backend en Python, para monitorear y gestionar un biodigestor.

La aplicación:

Permitirá a usuarios normales visualizar sensores en tiempo real (temperatura, pH y producción de biogás).

Permitirá a un administrador gestionar usuarios, gráficos y configuración del asistente de voz.

Se conectará con un módulo de Inteligencia Artificial (IA) desarrollado en Python, que analizará los datos y entregará recomendaciones al usuario mediante voz (TTS).

📖 2. Módulos y Requisitos Funcionales
🔑 Módulo de Autenticación y Cuentas

Login: acceso seguro con correo y contraseña.

Crear Cuenta: registro de nuevos usuarios.

Restablecer Contraseña.

Cerrar Sesión.

Eliminar Cuenta.

👤 Módulo para el Usuario Normal

Dashboard con 3 gráficos (MPAndroidChart):

Temperatura (barras).

pH (líneas).

Producción de biogás (circular).

Asistente de IA (TTS):

Analiza datos en tiempo real.

Clasifica estado como “bueno” o “malo”.

Da recomendaciones por voz.

⚙️ Módulo para el Administrador

Gestión de Gráficas: cambiar tipo de visualización (barras → circular, etc.) en tiempo real.

Configuración de Voz (TTS): cambiar voz del asistente para todos los usuarios.

Gestión de Usuarios:

Ver usuarios registrados.

Ver usuarios activos.

Ver usuarios bloqueados.

Bloquear/Desbloquear cuentas.

📖 3. Componentes Técnicos

Frontend:

Kotlin (Android Studio).

Librerías: MPAndroidChart (gráficas), Lottie (animaciones), TTS (Text-to-Speech).

Backend:

Python (Flask o FastAPI).

Librerías: FastAPI, SQLAlchemy, scikit-learn, pandas.

Base de Datos:

MySQL (almacena usuarios, lecturas de sensores, configuraciones de administrador).

Inteligencia Artificial:

Algoritmo: Árbol de Decisión (Decision Tree).

Librería: scikit-learn.

Datos: históricos del biodigestor o generados sintéticamente.