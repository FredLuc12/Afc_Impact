
#include <Arduino.h>
#include <Wire.h>
#include <SensirionI2cScd4x.h>

SensirionI2cScd4x scd4x;

const char* ssid = "IPhone de Alyssa";
const char* password = "azerty123";
const char* mqtt_server = "172.20.10.2"; // IP du Raspberry

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(10);
  }

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi connecté");
  client.setServer(mqtt_server, 1883);
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

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP8266_CO2")) {
      Serial.println("MQTT connecté");
    } else {
      delay(2000);
    }
  }
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

  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  String sensor_id = WiFi.macAddress();
  String payload = "{\"temperature\":25.5}";

  if (client.publish("capteurs/temp", sensor_id)) {
    Serial.println("Message envoyé");
  } else {
    Serial.println("Echec envoi");
  }

  delay(5000);

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
      Serial.print("Temp: ");
      Serial.print(temperature);
      Serial.print("humidity: ");
      Serial.print(humidity);

    }
  }

  delay(2000);
}
