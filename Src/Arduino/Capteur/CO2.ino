
#include <Arduino.h>
#include <Wire.h>
#include <SensirionI2cScd4x.h>

SensirionI2cScd4x scd4x;

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }

  // ESP8266: ajuster si besoin
  Wire.begin(D2, D1);           // SDA, SCL (NodeMCU : D2=GPIO4, D1=GPIO5)

  scd4x.begin(Wire, 0x62);
  
  uint16_t status;
  int16_t err = scd4x.performSelfTest(status);
  Serial.print("selfTest err="); Serial.print(err);
  Serial.print(" status="); Serial.println(status);      // adresse I2C de ton SCD41

  // int16_t err;

  // // Stopper les mesures périodiques au cas où
  // err = scd4x.stopPeriodicMeasurement();
  // if (err != 0) {
  //   Serial.print("stopPeriodicMeasurement error: ");
  //   Serial.println(err);
  //}
  delay(500);

  // Démarrer les mesures
  err = scd4x.startPeriodicMeasurement();
  if (err != 0) {
    Serial.print("startPeriodicMeasurement error: ");
    Serial.println(err);
  } else {
    Serial.println("SCD41 periodic measurement started");
  }

  // Temps pour que la première mesure soit prête
  delay(5000);
}

void loop() {
  int16_t err;
  bool dataReady = false;

  // Vérifier si une mesure est prête
  err = scd4x.getDataReadyStatus(dataReady);
  if (err != 0) {
    Serial.print("getDataReadyStatus error: ");
    Serial.println(err);
    delay(1000);
    return;
  }

  if (!dataReady) {
    delay(500);
    return;
  }

  uint16_t co2;
  float temperature;
  float humidity;

  err = scd4x.readMeasurement(co2, temperature, humidity);
  if (err != 0) {
    Serial.print("readMeasurement error: ");
    Serial.println(err);
  } else {
    if (co2 == 0) {
      Serial.println("Invalid sample (CO2 = 0), skipping");
    } else {
      Serial.print("CO2: ");
      Serial.print(co2);
      Serial.print(" ppm, Temp: ");
    }
  }

  delay(2000);
}
