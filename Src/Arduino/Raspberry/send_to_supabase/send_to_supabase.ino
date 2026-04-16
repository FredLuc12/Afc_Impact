#include <Arduino.h>
#include <Wire.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SensirionI2cScd4x.h>

// ----------- CONFIG -----------
const char* ssid = "iPhone de Alyssa";
const char* password = "azerty123";
const char* mqtt_server = "172.20.10.2";

// ----------- OBJETS -----------
WiFiClient espClient;
PubSubClient client(espClient);
SensirionI2cScd4x scd4x;

// ----------- WIFI -----------
void connectWiFi() {
  Serial.print("Connexion WiFi");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connecté !");
}

// ----------- MQTT -----------
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connexion MQTT...");

    if (client.connect("ESP8266_CO2")) {
      Serial.println("connecté !");
    } else {
      Serial.print("échec, rc=");
      Serial.print(client.state());
      Serial.println(" retry...");
      delay(2000);
    }
  }
}

// ----------- SETUP -----------
void setup() {
  Serial.begin(115200);

  connectWiFi();

  client.setServer(mqtt_server, 1883);

  // I2C
  Wire.begin(D2, D1);

  scd4x.begin(Wire, 0x62);

  delay(500);

  int16_t err = scd4x.startPeriodicMeasurement();
  if (err != 0) {
    Serial.print("Erreur startMeasurement: ");
    Serial.println(err);
  } else {
    Serial.println("Capteur démarré");
  }

  delay(5000); // attendre première mesure
}

// ----------- LOOP -----------
void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  bool dataReady = false;
  int16_t err = scd4x.getDataReadyStatus(dataReady);

  if (err != 0 || !dataReady) {
    delay(500);
    return;
  }

  uint16_t co2;
  float temperature;
  float humidity;

  err = scd4x.readMeasurement(co2, temperature, humidity);

  if (err != 0 || co2 == 0) {
    Serial.println("Erreur lecture capteur");
    delay(1000);
    return;
  }

  // ----------- PAYLOAD JSON -----------
  String mac = WiFi.macAddress();

  String payload = "{";
  payload += "\"name\":\"" + mac + "\",";
  payload += "\"type\":\"temperature\",";
  payload += "\"value\":" + String(temperature, 2);
  payload += "}";

  // ----------- ENVOI MQTT -----------
  if (client.publish("capteurs/temp", payload.c_str())) {
    Serial.println("Message envoyé :");
    Serial.println(payload);
  } else {
    Serial.println("Echec envoi MQTT");
  }

  delay(5000);
}