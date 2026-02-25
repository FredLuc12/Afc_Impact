#define PIR_PIN D2

void setup() {
  Serial.begin(115200);
  pinMode(PIR_PIN, INPUT);
  Serial.println("Test PIR en cours...");
}

void loop() {
  int motion = digitalRead(PIR_PIN);

  if (motion == HIGH) {
    Serial.println("Mouvement détecté !");
  } else {
    Serial.println("Pas de mouvement");
  }

  delay(1000);
}