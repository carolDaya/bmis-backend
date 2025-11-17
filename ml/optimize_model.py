# ml/optimize_model.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

def optimizar_modelo():
    """Optimiza el modelo para los casos problemáticos identificados"""
    
    print("🔄 OPTIMIZANDO MODELO...")
    
    # Cargar dataset original
    df = pd.read_csv("sensors.csv")
    
    # Preparación de datos (igual que antes)
    df["alerta_ia"] = (
        df["alerta_ia"].astype(str).str.lower()
        .map({"true": 1, "false": 0}).fillna(0).astype(int)
    )
    df["tipo_alerta"] = df["tipo_alerta"].fillna("Normal").astype(str)
    
    # 🔧 ESTRATEGIA 1: AUMENTAR DATOS PARA CASOS PROBLEMÁTICOS
    print("📊 Aumentando datos para casos problemáticos...")
    
    # Caso 1: Temperaturas bajas que no se detectan (25°C)
    temperaturas_bajas = df[
        (df['temperatura_celsius'] < 26) & 
        (df['alerta_ia'] == 1) &
        (df['tipo_alerta'] == 'Temperatura Anormal')
    ].copy()
    
    # Duplicar y variar ligeramente estos casos
    nuevas_temperaturas_bajas = []
    for _, row in temperaturas_bajas.iterrows():
        for _ in range(3):  # Triplicar estos casos críticos
            nueva_fila = row.copy()
            # Variación pequeña en características
            nueva_fila['temperatura_celsius'] += np.random.uniform(-1, 1)
            nueva_fila['presion_biogas_kpa'] += np.random.uniform(-10, 10)
            nueva_fila['mq4_ppm'] += np.random.uniform(-50, 50)
            nuevas_temperaturas_bajas.append(nueva_fila)
    
    # Caso 2: Baja producción confundida con temperatura
    bajas_produccion = df[
        (df['tipo_alerta'] == 'Baja Producción') & 
        (df['mq4_ppm'] < 2500)
    ].copy()
    
    nuevas_bajas_produccion = []
    for _, row in bajas_produccion.iterrows():
        for _ in range(4):  # Cuadruplicar estos casos raros
            nueva_fila = row.copy()
            # Mantener CH4 bajo pero variar otros parámetros
            nueva_fila['mq4_ppm'] = max(800, nueva_fila['mq4_ppm'] + np.random.uniform(-100, 100))
            nueva_fila['temperatura_celsius'] += np.random.uniform(-2, 2)
            nueva_fila['presion_biogas_kpa'] += np.random.uniform(-20, 20)
            nuevas_bajas_produccion.append(nueva_fila)
    
    # Combinar dataset aumentado
    df_aumentado = pd.concat([
        df,
        pd.DataFrame(nuevas_temperaturas_bajas),
        pd.DataFrame(nuevas_bajas_produccion)
    ], ignore_index=True)
    
    print(f"📈 Dataset original: {len(df)} registros")
    print(f"📈 Dataset aumentado: {len(df_aumentado)} registros")
    
    # 🔧 ESTRATEGIA 2: ENTRENAR CON PESOS DE CLASE MEJORADOS
    X = df_aumentado[["temperatura_celsius", "presion_biogas_kpa", "mq4_ppm", "dia_proceso"]]
    y_alerta = df_aumentado["alerta_ia"]
    y_tipo = df_aumentado["tipo_alerta"]
    
    # Calcular pesos de clase para manejar desbalanceo
    from sklearn.utils.class_weight import compute_class_weight
    
    # Pesos para modelo de alerta
    clases_alerta = y_alerta.unique()
    pesos_alerta = compute_class_weight(
        'balanced', 
        classes=clases_alerta, 
        y=y_alerta
    )
    peso_clases_alerta = dict(zip(clases_alerta, pesos_alerta))
    
    # Pesos para modelo de tipo
    clases_tipo = y_tipo.unique()
    pesos_tipo = compute_class_weight(
        'balanced',
        classes=clases_tipo,
        y=y_tipo
    )
    peso_clases_tipo = dict(zip(clases_tipo, pesos_tipo))
    
    print("⚖️  Pesos de clase calculados:")
    print(f"   Alerta: {peso_clases_alerta}")
    print(f"   Tipo: { {k: round(v, 2) for k, v in peso_clases_tipo.items()} }")
    
    # 🔧 ESTRATEGIA 3: MODELOS OPTIMIZADOS
    modelo_alerta_opt = RandomForestClassifier(
        n_estimators=150,  # Más árboles
        max_depth=20,      # Más profundidad
        min_samples_split=5,
        min_samples_leaf=2,
        class_weight=peso_clases_alerta,  # Usar pesos
        random_state=42,
        n_jobs=-1
    )
    
    modelo_tipo_opt = RandomForestClassifier(
        n_estimators=150,
        max_depth=20,
        min_samples_split=5, 
        min_samples_leaf=2,
        class_weight=peso_clases_tipo,  # Usar pesos
        random_state=42,
        n_jobs=-1
    )
    
    # Entrenamiento
    print("🤖 Entrenando modelos optimizados...")
    modelo_alerta_opt.fit(X, y_alerta)
    modelo_tipo_opt.fit(X, y_tipo)
    
    # Guardar modelos optimizados
    joblib.dump(modelo_alerta_opt, "ml/modelo_alerta_optimizado.pkl")
    joblib.dump(modelo_tipo_opt, "ml/modelo_tipo_alerta_optimizado.pkl")
    
    print("✅ Modelos optimizados guardados")
    return modelo_alerta_opt, modelo_tipo_opt, df_aumentado

if __name__ == "__main__":
    optimizar_modelo()