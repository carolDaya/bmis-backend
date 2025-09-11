import pandas as pd

def cargar_y_procesar_datos(ruta_excel):
    df = pd.read_excel(ruta_excel)
    
    df = df.rename(columns={
        'timestamp': 'Fecha y Hora',
        'dia_proceso': 'Día',
        'fase_proceso': 'Fase del Proceso',
        'temperatura_celsius': 'Temperatura (°C)',
        'presion_biogas_kpa': 'Presión (kPa)',
        'volumen_biogas_m3_dia': 'Volumen de Biogás (m3/día)',
        'alerta_ia': 'Alerta IA',
        'tipo_alerta': 'Tipo de Alerta'
    })
    
    df['Fase del Proceso Numérica'] = df['Fase del Proceso'].map({'Activa': 1, 'Inactiva': 0})
    
    return df
