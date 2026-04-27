#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN D4       
#define DHTTYPE DHT11  

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  Serial.println("Test DHT11...");
  dht.begin();
}

void loop() {
  delay(2000);  // Attendre 2 secondes entre chaque lecture

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Erreur lecture DHT11 !");
    return;
  }

  Serial.print("Humidité: ");
  Serial.print(humidity);
  Serial.print(" %\t");

  Serial.print("Température: ");
  Serial.print(temperature);
  Serial.println(" °C");
}

