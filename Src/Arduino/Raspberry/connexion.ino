#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "RSPI_PM";
const char* password = "12345678";
const char* mqtt_server = "10.42.0.1"; // IP du Raspberry

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  
  Serial.println(WiFi.scanNetworks());

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("WiFi connecté");

  client.setServer(mqtt_server, 1883);
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

  if (!client.connected()) {
    reconnect();
  }

  client.loop();

  if (client.publish("capteurs/co2", "750")) {
    Serial.println("Message envoyé");
  } else {
    Serial.println("Echec envoi");
  }

  delay(5000);
}