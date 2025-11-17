# ml/ensemble_system.py
import joblib
import pandas as pd
import numpy as np

class SistemaAlertaOptimizado:
    def __init__(self):
        self.modelo_original_alerta = joblib.load("ml/modelo_alerta.pkl")
        self.modelo_original_tipo = joblib.load("ml/modelo_tipo_alerta.pkl")
        
        try:
            self.modelo_optimizado_alerta = joblib.load("ml/modelo_alerta_optimizado.pkl")
            self.modelo_optimizado_tipo = joblib.load("ml/modelo_tipo_alerta_optimizado.pkl")
            self.usar_optimizado = True
        except:
            self.usar_optimizado = False
    
    def predecir_con_ensemble(self, datos):
        """Sistema ensemble que combina modelos + reglas de negocio"""
        
        # Convertir a DataFrame si es necesario
        if isinstance(datos, (list, np.ndarray)):
            datos = pd.DataFrame([datos], 
                               columns=["temperatura_celsius", "presion_biogas_kpa", 
                                       "mq4_ppm", "dia_proceso"])
        
        # 🔧 REGLA 1: DETECCIÓN OBLIGATORIA DE TEMPERATURA EXTREMA
        temperatura = datos['temperatura_celsius'].iloc[0]
        presion = datos['presion_biogas_kpa'].iloc[0]
        ch4 = datos['mq4_ppm'].iloc[0]
        dia = datos['dia_proceso'].iloc[0]
        
        # Reglas de negocio explícitas
        alertas_reglas = []
        
        # Temperaturas críticas (OBLIGATORIO alertar)
        if temperatura < 26 or temperatura > 39:
            alertas_reglas.append({
                'tipo': 'Temperatura Anormal',
                'confianza': 0.95,
                'fuente': 'regla'
            })
        
        # Baja producción (CH4 muy bajo después de día 7)
        if ch4 < 2500 and dia > 7:
            alertas_reglas.append({
                'tipo': 'Baja Producción', 
                'confianza': 0.85,
                'fuente': 'regla'
            })
        
        # Presión crítica
        if presion > 780:
            alertas_reglas.append({
                'tipo': 'Presión Crítica',
                'confianza': 0.90,
                'fuente': 'regla'
            })
        
        # 🔧 PREDICCIÓN CON MÚLTIPLES MODELOS
        pred_original_alerta = self.modelo_original_alerta.predict(datos)[0]
        pred_original_tipo = self.modelo_original_tipo.predict(datos)[0] if pred_original_alerta else "Normal"
        
        if self.usar_optimizado:
            pred_optimizado_alerta = self.modelo_optimizado_alerta.predict(datos)[0]
            pred_optimizado_tipo = self.modelo_optimizado_tipo.predict(datos)[0] if pred_optimizado_alerta else "Normal"
        else:
            pred_optimizado_alerta = pred_original_alerta
            pred_optimizado_tipo = pred_original_tipo
        
        # 🔧 COMBINAR PREDICCIONES
        # Votación para alerta
        votos_alerta = [pred_original_alerta, pred_optimizado_alerta]
        if alertas_reglas:
            votos_alerta.append(1)  # Las reglas siempre votan por alerta
        
        alerta_final = 1 if sum(votos_alerta) >= 2 else 0
        
        # Determinar tipo de alerta
        if not alerta_final:
            tipo_final = "Normal"
            fuente = "modelo"
        else:
            # Priorizar reglas de negocio
            if alertas_reglas:
                # Tomar la alerta de mayor confianza de las reglas
                alerta_principal = max(alertas_reglas, key=lambda x: x['confianza'])
                tipo_final = alerta_principal['tipo']
                fuente = alerta_principal['fuente']
            else:
                # Votación entre modelos
                tipos = [pred_original_tipo, pred_optimizado_tipo]
                tipo_final = max(set(tipos), key=tipos.count)
                fuente = "modelo"
        
        return {
            'alerta': alerta_final,
            'tipo_alerta': tipo_final,
            'fuente': fuente,
            'detalles': {
                'original': {'alerta': pred_original_alerta, 'tipo': pred_original_tipo},
                'optimizado': {'alerta': pred_optimizado_alerta, 'tipo': pred_optimizado_tipo},
                'reglas': alertas_reglas
            }
        }

# Prueba del sistema optimizado
def probar_sistema_optimizado():
    """Prueba el sistema optimizado con los casos problemáticos"""
    
    sistema = SistemaAlertaOptimizado()
    
    casos_problematicos = [
        {
            'nombre': 'Temperatura Baja (25°C) - Caso Problemático',
            'datos': [25.0, 500.0, 5200.0, 13]
        },
        {
            'nombre': 'Baja Producción (1800 ppm) - Caso Problemático', 
            'datos': [36.0, 600.0, 1800.0, 21]
        },
        {
            'nombre': 'Caso Normal (36.5°C)',
            'datos': [36.5, 350.0, 5200.0, 12]
        },
        {
            'nombre': 'Presión Crítica',
            'datos': [37.0, 1180.0, 6500.0, 28]
        }
    ]
    
    print("🧪 PROBANDO SISTEMA OPTIMIZADO")
    print("=" * 50)
    
    for caso in casos_problematicos:
        resultado = sistema.predecir_con_ensemble(caso['datos'])
        
        print(f"\n📋 {caso['nombre']}:")
        print(f"   Datos: Temp {caso['datos'][0]}°C, Presión {caso['datos'][1]} kPa, CH4 {caso['datos'][2]} ppm")
        print(f"   🔮 Resultado: Alerta {'SÍ' if resultado['alerta'] else 'NO'} - {resultado['tipo_alerta']}")
        print(f"   📍 Fuente: {resultado['fuente']}")
        
        if resultado['detalles']['reglas']:
            print(f"   ⚡ Reglas activadas: {[r['tipo'] for r in resultado['detalles']['reglas']]}")

if __name__ == "__main__":
    probar_sistema_optimizado()