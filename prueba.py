from services.ai_service import predecir_alerta

# CASO 1: Valores normales al inicio del proceso
resultado1 = predecir_alerta(
    temperatura=36.8,
    presion=2.0,
    gas=300,
    timestamp="2025-01-01 02:00:00"
)
print("Caso 1:", resultado1)

# CASO 2: Temperatura baja (alerta)
resultado2 = predecir_alerta(
    temperatura=32.5,
    presion=2.1,
    gas=310,
    timestamp="2025-01-01 04:00:00"
)
print("Caso 2:", resultado2)

# CASO 3: Gas alto (alerta)
resultado3 = predecir_alerta(
    temperatura=37.0,
    presion=2.0,
    gas=700,
    timestamp="2025-01-02 03:00:00"
)
print("Caso 3:", resultado3)

# CASO 4: Presión baja (alerta)
resultado4 = predecir_alerta(
    temperatura=36.5,
    presion=1.2,
    gas=310,
    timestamp="2025-01-03 05:00:00"
)
print("Caso 4:", resultado4)

# CASO 5: Valores normales pero fase final del proceso
resultado5 = predecir_alerta(
    temperatura=36.0,
    presion=2.3,
    gas=100,
    timestamp="2025-01-28 23:00:00"
)
print("Caso 5:", resultado5)
