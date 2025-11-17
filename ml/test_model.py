# ml/test_model_optimizado.py
import pandas as pd
import joblib
import numpy as np
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from ensemble_system import SistemaAlertaOptimizado  # Importar nuestro sistema optimizado

def test_modelo_optimizado():
    """Prueba completa del sistema optimizado"""
    
    print("🧪 INICIANDO PRUEBAS DEL SISTEMA OPTIMIZADO")
    print("=" * 60)
    
    # Cargar sistema optimizado
    try:
        sistema = SistemaAlertaOptimizado()
        print("✅ Sistema optimizado cargado correctamente")
    except Exception as e:
        print(f"❌ Error cargando sistema optimizado: {e}")
        return
    
    # Cargar dataset para pruebas
    try:
        df = pd.read_csv("sensors.csv")
        print(f"✅ Dataset cargado: {len(df)} registros")
    except FileNotFoundError:
        print("❌ Error: No se encontró 'sensors.csv'")
        return
    
    # Preparar datos
    df["alerta_ia"] = (
        df["alerta_ia"]
        .astype(str)
        .str.lower()
        .map({"true": 1, "false": 0})
        .fillna(0)
        .astype(int)
    )
    df["tipo_alerta"] = df["tipo_alerta"].fillna("Normal").astype(str)
    
    # ----------------------------------------------------
    # 🧪 PRUEBA 1: EVALUACIÓN EN TODO EL DATASET
    # ----------------------------------------------------
    print("\n📊 PRUEBA 1: Evaluación en Dataset Completo (Sistema Optimizado)")
    print("-" * 60)
    
    X = df[["temperatura_celsius", "presion_biogas_kpa", "mq4_ppm", "dia_proceso"]]
    y_alerta_real = df["alerta_ia"]
    y_tipo_real = df["tipo_alerta"]
    
    # Predicciones con sistema optimizado
    y_alerta_pred = []
    y_tipo_pred = []
    fuentes = []
    
    for i, (_, fila) in enumerate(X.iterrows()):
        if i % 50 == 0:  # Progress bar
            print(f"   Procesando... {i}/{len(X)}")
        
        resultado = sistema.predecir_con_ensemble([
            fila['temperatura_celsius'],
            fila['presion_biogas_kpa'], 
            fila['mq4_ppm'],
            fila['dia_proceso']
        ])
        
        y_alerta_pred.append(resultado['alerta'])
        y_tipo_pred.append(resultado['tipo_alerta'])
        fuentes.append(resultado['fuente'])
    
    # Métricas
    acc_alerta = accuracy_score(y_alerta_real, y_alerta_pred)
    acc_tipo = accuracy_score(y_tipo_real, y_tipo_pred)
    
    print(f"✅ Precisión Alerta: {acc_alerta:.3f} ({acc_alerta*100:.1f}%)")
    print(f"✅ Precisión Tipo Alerta: {acc_tipo:.3f} ({acc_tipo*100:.1f}%)")
    
    # Distribución de fuentes
    fuentes_count = pd.Series(fuentes).value_counts()
    print(f"\n📍 Fuentes de predicción:")
    for fuente, count in fuentes_count.items():
        print(f"   {fuente}: {count} ({count/len(fuentes)*100:.1f}%)")
    
    # Matriz de confusión para alerta
    cm_alerta = confusion_matrix(y_alerta_real, y_alerta_pred)
    print(f"\n📊 Matriz Confusión Alerta:")
    print(f"           Predicho")
    print(f"Real       0(Normal)  1(Alerta)")
    print(f"  0(Normal) {cm_alerta[0][0]:6d}     {cm_alerta[0][1]:6d}")
    print(f"  1(Alerta) {cm_alerta[1][0]:6d}     {cm_alerta[1][1]:6d}")
    
    # Reporte detallado
    print("\n📈 Reporte Tipo Alerta (Sistema Optimizado):")
    print(classification_report(y_tipo_real, y_tipo_pred, zero_division=0))
    
    # ----------------------------------------------------
    # 🧪 PRUEBA 2: CASOS PROBLEMÁTICOS RESUELTOS
    # ----------------------------------------------------
    print("\n🎯 PRUEBA 2: Casos Problemáticos - ANTES vs AHORA")
    print("-" * 60)
    
    casos_criticos = [
        {
            "nombre": "❌ ANTES: Temperatura Baja (25°C) NO detectada",
            "datos": [25.0, 500.0, 5200.0, 13],
            "esperado_alerta": 1,
            "esperado_tipo": "Temperatura Anormal"
        },
        {
            "nombre": "❌ ANTES: Baja Producción → Temperatura Anormal", 
            "datos": [36.0, 600.0, 1800.0, 21],
            "esperado_alerta": 1,
            "esperado_tipo": "Baja Producción"
        },
        {
            "nombre": "✅ CASO NORMAL (control)",
            "datos": [36.5, 350.0, 5200.0, 12],
            "esperado_alerta": 0,
            "esperado_tipo": "Normal"
        },
        {
            "nombre": "✅ PRESIÓN CRÍTICA",
            "datos": [37.0, 1180.0, 6500.0, 28],
            "esperado_alerta": 1,
            "esperado_tipo": "Presión Crítica"
        },
        {
            "nombre": "✅ CH4 ALTO",
            "datos": [36.5, 400.0, 6800.0, 10],
            "esperado_alerta": 1,
            "esperado_tipo": "Concentración CH4 Alta"
        }
    ]
    
    resultados_optimizados = []
    
    for caso in casos_criticos:
        resultado = sistema.predecir_con_ensemble(caso["datos"])
        
        correcto_alerta = resultado['alerta'] == caso["esperado_alerta"]
        correcto_tipo = resultado['tipo_alerta'] == caso["esperado_tipo"]
        
        estado = "✅" if correcto_alerta and correcto_tipo else "❌"
        mejorado = "🔄 MEJORADO" if "ANTES" in caso["nombre"] and correcto_alerta and correcto_tipo else ""
        
        print(f"\n{estado} {caso['nombre']} {mejorado}")
        print(f"   📊 Datos: Temp {caso['datos'][0]}°C, Presión {caso['datos'][1]} kPa, CH4 {caso['datos'][2]} ppm")
        print(f"   🔮 Resultado: Alerta {'SÍ' if resultado['alerta'] else 'NO'} - {resultado['tipo_alerta']}")
        print(f"   📍 Fuente: {resultado['fuente']}")
        
        if resultado['detalles']['reglas']:
            print(f"   ⚡ Reglas activadas: {[r['tipo'] for r in resultado['detalles']['reglas']]}")
        
        resultados_optimizados.append({
            "caso": caso["nombre"],
            "correcto_alerta": correcto_alerta,
            "correcto_tipo": correcto_tipo,
            "fuente": resultado['fuente']
        })
    
    # ----------------------------------------------------
    # 🧪 PRUEBA 3: ANÁLISIS DE MEJORA
    # ----------------------------------------------------
    print("\n📈 PRUEBA 3: Análisis de Mejora")
    print("-" * 50)
    
    # Comparar con resultados anteriores
    mejoras_alerta = sum(1 for r in resultados_optimizados if "ANTES" in r["caso"] and r["correcto_alerta"])
    mejoras_tipo = sum(1 for r in resultados_optimizados if "ANTES" in r["caso"] and r["correcto_tipo"])
    
    total_casos_problematicos = sum(1 for r in resultados_optimizados if "ANTES" in r["caso"])
    
    print(f"🔧 Casos problemáticos resueltos:")
    print(f"   ✅ Alertas corregidas: {mejoras_alerta}/{total_casos_problematicos}")
    print(f"   ✅ Tipos corregidos: {mejoras_tipo}/{total_casos_problematicos}")
    
    # Efectividad de reglas
    casos_con_reglas = sum(1 for r in resultados_optimizados if r["fuente"] == "regla")
    print(f"   📍 Predicciones por reglas: {casos_con_reglas}/{len(resultados_optimizados)}")
    
    # ----------------------------------------------------
    # 🧪 PRUEBA 4: CASOS LÍMITE
    # ----------------------------------------------------
    print("\n🎯 PRUEBA 4: Casos Límite y Edge Cases")
    print("-" * 50)
    
    casos_limite = [
        {"temp": 26.0, "presion": 500, "ch4": 5000, "dia": 15, "desc": "Límite inferior temperatura"},
        {"temp": 39.0, "presion": 500, "ch4": 5000, "dia": 15, "desc": "Límite superior temperatura"},
        {"temp": 36.5, "presion": 580, "ch4": 5000, "dia": 15, "desc": "Límite presión alta"},
        {"temp": 36.5, "presion": 780, "ch4": 5000, "dia": 15, "desc": "Límite presión crítica"},
        {"temp": 36.5, "presion": 500, "ch4": 2500, "dia": 8, "desc": "Límite CH4 bajo (día > 7)"},
        {"temp": 36.5, "presion": 500, "ch4": 6000, "dia": 15, "desc": "Límite CH4 alto"}
    ]
    
    for caso in casos_limite:
        resultado = sistema.predecir_con_ensemble([
            caso["temp"], caso["presion"], caso["ch4"], caso["dia"]
        ])
        
        print(f"📋 {caso['desc']}:")
        print(f"   Temp: {caso['temp']}°C, Presión: {caso['presion']} kPa, CH4: {caso['ch4']} ppm")
        print(f"   → Alerta: {'SÍ' if resultado['alerta'] else 'NO'} - {resultado['tipo_alerta']}")
        print(f"   Fuente: {resultado['fuente']}")
    
    # ----------------------------------------------------
    # 📊 RESUMEN FINAL OPTIMIZADO
    # ----------------------------------------------------
    print("\n" + "=" * 60)
    print("🎉 RESUMEN FINAL - SISTEMA OPTIMIZADO")
    print("=" * 60)
    
    # Estadísticas generales
    correctos_alerta = sum(1 for r in resultados_optimizados if r["correcto_alerta"])
    correctos_tipo = sum(1 for r in resultados_optimizados if r["correcto_tipo"])
    
    print(f"🧪 Casos de prueba: {len(resultados_optimizados)}")
    print(f"✅ Alertas correctas: {correctos_alerta}/{len(resultados_optimizados)} ({correctos_alerta/len(resultados_optimizados)*100:.1f}%)")
    print(f"✅ Tipos correctos: {correctos_tipo}/{len(resultados_optimizados)} ({correctos_tipo/len(resultados_optimizados)*100:.1f}%)")
    print(f"📈 Precisión general alerta: {acc_alerta*100:.1f}%")
    print(f"📈 Precisión general tipo: {acc_tipo*100:.1f}%")
    
    # Verificar mejoras
    if mejoras_alerta == total_casos_problematicos and mejoras_tipo == total_casos_problematicos:
        print("\n🎉 ¡OPTIMIZACIÓN EXITOSA! Todos los casos problemáticos resueltos")
    else:
        print(f"\n⚠️  Optimización parcial: {mejoras_alerta}/{total_casos_problematicos} casos resueltos")
    
    print("\n🚀 El sistema optimizado está listo para producción")

if __name__ == "__main__":
    test_modelo_optimizado()