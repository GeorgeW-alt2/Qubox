const int ledPin = 10; 
int ledState = LOW; 
unsigned long previousMillis = 0; 
const long interval = 50;  
void setup() {
  pinMode(ledPin, OUTPUT);
}
void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    if (ledState == LOW) {
      ledState = HIGH;
    } else {
      ledState = LOW;
    }
    digitalWrite(ledPin, ledState);
  }
}
