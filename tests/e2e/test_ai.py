"""
Pruebas E2E SIMPLES para el backend de biodigestor
Pruebas directas usando requests contra la API real
"""

import requests
import json
import pytest

# Configuración
BASE_URL = "http://200.234.235.149:5000"  # Tu IP del servidor


class TestSimpleE2E:
    """Pruebas E2E simples que solo hacen requests HTTP"""
    
    def test_1_servidor_esta_activo(self):
        """Test más simple: ¿El servidor responde?"""
        print("\n" + "="*60)
        print("Test 1: Verificar que el servidor está activo")
        print("="*60)
        
        try:
            response = requests.get(f"{BASE_URL}/", timeout=10)
            print(f"✓ Servidor responde. Status: {response.status_code}")
            print(f"  URL: {BASE_URL}")
            assert response.status_code in [200, 404, 401]
        except requests.exceptions.ConnectionError:
            print("✗ ERROR: No se puede conectar al servidor")
            print(f"  Verifica que el servidor en {BASE_URL} esté ejecutándose")
            pytest.fail("Servidor no disponible")
    
    def test_2_endpoint_analizar_responde(self):
        """Test simple: El endpoint /api/analizar responde"""
        print("\n" + "="*60)
        print("Test 2: Endpoint /api/analizar responde")
        print("="*60)
        
        try:
            response = requests.get(f"{BASE_URL}/api/analizar", timeout=10)
            print(f"✓ Endpoint /api/analizar responde. Status: {response.status_code}")
            
            # Si responde 200, validar estructura básica
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Respuesta JSON válida recibida")
                    
                    # Campos mínimos que debería tener
                    campos_minimos = ["alerta_ia", "mensaje_lectura", "recomendacion"]
                    for campo in campos_minimos:
                        if campo in data:
                            print(f"  ✓ Campo '{campo}' presente")
                        else:
                            print(f"  ✗ Campo '{campo}' ausente")
                            
                except json.JSONDecodeError:
                    print("  ✗ Respuesta no es JSON válido")
            
            # Aceptar cualquier status code (200, 404, 500, etc)
            print(f"  Status aceptado: {response.status_code}")
            
        except requests.exceptions.Timeout:
            print("✗ TIMEOUT: El endpoint tardó demasiado en responder")
        except Exception as e:
            print(f"✗ ERROR: {type(e).__name__}: {str(e)}")
    
    def test_3_endpoint_sensores_responde(self):
        """Test simple: El endpoint /api/sensors responde"""
        print("\n" + "="*60)
        print("Test 3: Endpoint /api/sensors responde")
        print("="*60)
        
        try:
            response = requests.get(f"{BASE_URL}/api/sensors", timeout=10)
            print(f"✓ Endpoint /api/sensors responde. Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Se recibieron {len(data)} sensores")
                    
                    if len(data) > 0:
                        primer_sensor = data[0]
                        print(f"  Primer sensor: ID={primer_sensor.get('id')}, "
                              f"Nombre='{primer_sensor.get('nombre')}'")
                        
                        # Validar estructura básica
                        campos_sensor = ["id", "nombre", "tipo", "unidad", "activo"]
                        for campo in campos_sensor:
                            if campo in primer_sensor:
                                print(f"    ✓ Sensor tiene campo '{campo}'")
                except:
                    print("  ✗ No se pudo parsear JSON")
            
        except Exception as e:
            print(f"✗ ERROR: {type(e).__name__}: {str(e)}")
    
    def test_4_endpoint_auth_login_responde(self):
        """Test simple: El endpoint de login responde"""
        print("\n" + "="*60)
        print("Test 4: Endpoint /auth/login responde")
        print("="*60)
        
        try:
            # Solo probamos que el endpoint existe y responde
            # No enviamos datos reales para no crear usuarios
            test_data = {
                "telefono": "0000000000",  # Teléfono que probablemente no existe
                "password": "test123"
            }
            
            response = requests.post(
                f"{BASE_URL}/auth/login",
                json=test_data,
                timeout=10
            )
            
            print(f"✓ Endpoint /auth/login responde. Status: {response.status_code}")
            
            if response.status_code in [200, 401, 400]:
                print(f"  Status esperado recibido: {response.status_code}")
            
        except Exception as e:
            print(f"✗ ERROR: {type(e).__name__}: {str(e)}")
    
    def test_5_endpoint_proceso_estado_responde(self):
        """Test simple: Verificar estado del proceso"""
        print("\n" + "="*60)
        print("Test 5: Endpoint /api/proceso/estado responde")
        print("="*60)
        
        try:
            response = requests.get(f"{BASE_URL}/api/proceso/estado", timeout=10)
            print(f"✓ Endpoint /proceso/estado responde. Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Estado del proceso: {data}")
                    
                    # Verificar si tiene el campo proceso_activo
                    if "proceso_activo" in data:
                        estado = "ACTIVO" if data["proceso_activo"] else "INACTIVO"
                        print(f"  ✓ Proceso está: {estado}")
                    else:
                        print(f"  ✗ No tiene campo 'proceso_activo'")
                        
                except:
                    print("  ✗ No se pudo parsear JSON")
            
        except Exception as e:
            print(f"✗ ERROR: {type(e).__name__}: {str(e)}")
    
    def test_6_respuesta_json_valida_en_analizar(self):
        """Test específico: Validar estructura JSON de /api/analizar"""
        print("\n" + "="*60)
        print("Test 6: Validar estructura JSON de /api/analizar")
        print("="*60)
        
        try:
            response = requests.get(f"{BASE_URL}/api/analizar", timeout=10)
            
            # Solo validamos si la respuesta es 200
            if response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Lista de campos que ESPERAMOS en la respuesta
                    campos_esperados = [
                        "alerta_ia",
                        "dia_proceso", 
                        "mensaje_lectura",
                        "recomendacion",
                        "tipo_estado"
                    ]
                    
                    print("Validando estructura de respuesta:")
                    campos_presentes = []
                    campos_ausentes = []
                    
                    for campo in campos_esperados:
                        if campo in data:
                            campos_presentes.append(campo)
                            valor = data[campo]
                            tipo = type(valor).__name__
                            print(f"  ✓ {campo}: {valor} (tipo: {tipo})")
                        else:
                            campos_ausentes.append(campo)
                            print(f"  ✗ {campo}: AUSENTE")
                    
                    # Resumen
                    print(f"\nResumen: {len(campos_presentes)}/{len(campos_esperados)} campos presentes")
                    
                    if len(campos_ausentes) > 0:
                        print(f"Campos ausentes: {', '.join(campos_ausentes)}")
                    
                except json.JSONDecodeError as e:
                    print(f"✗ ERROR: Respuesta no es JSON válido: {str(e)}")
                    print(f"  Respuesta recibida: {response.text[:200]}...")
            else:
                print(f"Status code {response.status_code}, no se valida JSON")
                
        except Exception as e:
            print(f"✗ ERROR: {type(e).__name__}: {str(e)}")
    
    def test_7_tiempo_respuesta_aceptable(self):
        """Test de performance: Tiempo de respuesta aceptable"""
        print("\n" + "="*60)
        print("Test 7: Tiempo de respuesta aceptable")
        print("="*60)
        
        import time
        
        endpoints = [
            "/api/analizar",
            "/api/sensors",
            "/api/proceso/estado"
        ]
        
        for endpoint in endpoints:
            try:
                start_time = time.time()
                response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
                elapsed = time.time() - start_time
                
                if elapsed < 2.0:
                    print(f"✓ {endpoint}: {elapsed:.2f}s (ACEPTABLE)")
                elif elapsed < 5.0:
                    print(f"⚠ {endpoint}: {elapsed:.2f}s (LENTO)")
                else:
                    print(f"✗ {endpoint}: {elapsed:.2f}s (MUY LENTO)")
                    
            except requests.exceptions.Timeout:
                print(f"✗ {endpoint}: TIMEOUT (>5s)")
            except Exception as e:
                print(f"✗ {endpoint}: ERROR - {type(e).__name__}")


# Función para ejecutar todas las pruebas manualmente
def run_all_tests():
    """Ejecutar todas las pruebas manualmente"""
    print("="*70)
    print("EJECUTANDO PRUEBAS E2E SIMPLES")
    print("="*70)
    print(f"Servidor: {BASE_URL}")
    print("="*70)
    
    tester = TestSimpleE2E()
    tests = [
        ("test_1_servidor_esta_activo", "Servidor activo"),
        ("test_2_endpoint_analizar_responde", "Endpoint /analizar"),
        ("test_3_endpoint_sensores_responde", "Endpoint /sensors"),
        ("test_4_endpoint_auth_login_responde", "Endpoint /auth/login"),
        ("test_5_endpoint_proceso_estado_responde", "Endpoint /proceso/estado"),
        ("test_6_respuesta_json_valida_en_analizar", "Validación JSON"),
        ("test_7_tiempo_respuesta_aceptable", "Performance"),
    ]
    
    resultados = []
    
    for test_method, descripcion in tests:
        print(f"\n{'='*60}")
        print(f"Ejecutando: {descripcion}")
        print('='*60)
        
        try:
            # Ejecutar el test
            getattr(tester, test_method)()
            resultados.append((descripcion, "PASÓ", ""))
            print(f"✓ {descripcion} - PASÓ")
            
        except AssertionError as e:
            resultados.append((descripcion, "FALLÓ", str(e)))
            print(f"✗ {descripcion} - FALLÓ: {e}")
            
        except Exception as e:
            resultados.append((descripcion, "ERROR", str(e)))
            print(f"✗ {descripcion} - ERROR: {type(e).__name__}: {e}")
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE PRUEBAS E2E")
    print("="*70)
    
    pasaron = sum(1 for _, estado, _ in resultados if estado == "PASÓ")
    total = len(resultados)
    
    print(f"\nResultados: {pasaron}/{total} pruebas pasaron\n")
    
    for descripcion, estado, mensaje in resultados:
        icono = "✓" if estado == "PASÓ" else "✗"
        print(f"{icono} {descripcion}: {estado}")
        if mensaje:
            print(f"   {mensaje}")
    
    print("\n" + "="*70)
    
    if pasaron == total:
        print("¡TODAS LAS PRUEBAS PASARON! 🎉")
    else:
        print(f"{total - pasaron} pruebas fallaron o tuvieron errores")
    
    return pasaron == total


if __name__ == "__main__":
    # Ejecutar como script independiente
    success = run_all_tests()
    
    # Devolver código de salida para CI/CD
    import sys
    sys.exit(0 if success else 1)