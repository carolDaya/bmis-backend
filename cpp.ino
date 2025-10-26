#include <WiFi.h>
#include <HTTPClient.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// =============================
// CONFIGURACIÓN DE RED WiFi
// =============================
const char* ssid = "Funcionarios";
const char* password = "SomosSena_2025";

// IP del servidor Flask (ajústala según tu red)
const char* host = "10.9.191.194"; 
const int port = 5000;

// =============================
// CONFIGURACIÓN DE SENSORES
// =============================

// DS18B20
#define ONE_WIRE_BUS 32
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensorTemp(&oneWire);

// MQ-4 (Analógico)
#define MQ4_PIN 35

// Sensor de presión (Analógico)
#define PRESION_PIN 34

// =============================
// CONFIGURACIÓN LCD 20x4
// =============================
LiquidCrystal_I2C lcd(0x27, 20, 4);

// =============================
// CONSTANTES DE CONVERSIÓN
// =============================
// Factor de conversión para la presión: 1 MPa ≈ 145.038 psi
const float MPA_A_PSI = 145.038; 

// =============================
// FUNCIONES DE CONVERSIÓN
// =============================

// Función de conversión aproximada de lectura analógica (0-4095) del MQ-4 a PPM.
// Nota: Esta es una simplificación. Una calibración precisa requiere más datos y puede usar 
// la curva de respuesta del datasheet y la resistencia de carga.
float convertirMQ4aPPM(int valorAnalogico) {
  // Ajusta la pendiente y la intersección según la calibración de tu sensor 
  // y el gas específico (metano en el caso del MQ-4).
  // Se usa una relación lineal simple para el ejemplo (0-4095 -> 0-10000 ppm).
  // Un valor de 0 a 10000 ppm es un rango común para este tipo de sensor.
  float ppm = (valorAnalogico / 4095.0) * 10000.0; 
  return ppm;
}

// =============================
// SETUP
// =============================
void setup() {
  Serial.begin(115200);

  // Iniciar LCD
  Wire.begin(21, 19);  // SDA=21, SCL=19 (ajusta según tu conexión)
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0, 0);
  lcd.print("Iniciando Sistema...");
  lcd.setCursor(0, 1);
  lcd.print("Conectando WiFi...");

  // Iniciar sensores
  sensorTemp.begin();

  // Conectar WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi Conectado!");
  lcd.setCursor(0, 1);
  lcd.print("IP: ");
  lcd.print(WiFi.localIP());
  delay(2000);
  lcd.clear();
}

// =============================
// LOOP PRINCIPAL
// =============================
void loop() {
  sensorTemp.requestTemperatures();

  // Leer valores de sensores
  float temperatura = sensorTemp.getTempCByIndex(0);
  int gasAnalogico = analogRead(MQ4_PIN);
  float gasPPM = convertirMQ4aPPM(gasAnalogico);
  
  // Conversión de presión: 
  // 1. Convertir el valor analógico a MPa (manteniendo la lógica original):
  float presionMPa = analogRead(PRESION_PIN) * (1.2 / 4095.0); 
  // 2. Convertir de MPa a PSI:
  float presionPSI = presionMPa * MPA_A_PSI; 

  // Mostrar en monitor serial
  Serial.println("----- Lectura Actual -----");
  Serial.print("Temperatura: "); Serial.print(temperatura); Serial.println(" °C");
  Serial.print("Gas: "); Serial.print(gasPPM); Serial.println(" ppm");
  Serial.print("Presion: "); Serial.print(presionPSI); Serial.println(" psi");

  // Mostrar en LCD
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temp: "); lcd.print(temperatura, 1); lcd.print((char)223); lcd.print("C");
  
  lcd.setCursor(0, 1);
  lcd.print("Gas: "); lcd.print(gasPPM, 0); lcd.print("ppm"); // Mostrar en ppm
  
  lcd.setCursor(0, 2);
  lcd.print("Presion: "); lcd.print(presionPSI, 1); lcd.print("psi"); // Mostrar en psi

  // Enviar datos al servidor Flask
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    // Se recomienda enviar los datos con las unidades esperadas por el servidor. 
    // Si el servidor espera MPa, usa presionMPa. Si espera ppm, usa gasPPM.
    // Aquí usamos los valores convertidos (ppm y psi) para el ejemplo.
    String url = "http://" + String(host) + ":" + String(port) + "/api/lecturas?temp=" 
               + String(temperatura, 2) + "&gas=" + String(gasPPM, 0) // Enviando ppm
               + "&presion=" + String(presionPSI, 1); // Enviando psi

    http.begin(url);
    int httpResponseCode = http.GET();

    lcd.setCursor(0, 3);
    if (httpResponseCode > 0) {
      lcd.print("Envio OK ");
      lcd.print(httpResponseCode);
      Serial.println("✅ Envio exitoso al servidor.");
    } else {
      lcd.print("Error envio!");
      Serial.println("❌ Error en envio HTTP");
    }
    http.end();
  } else {
    lcd.setCursor(0, 3);
    lcd.print("WiFi desconectado!");
    Serial.println("WiFi no conectado.");
  }

  delay(5000); // Esperar 5 segundos antes de la siguiente lectura
}