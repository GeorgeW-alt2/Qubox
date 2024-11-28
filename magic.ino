//Random number generator
//Use a series of glass diodes.
int sensorPin = A0;   // select the input pin for the glass diodes
int sensorValue = 0;  // variable to store the value coming from the sensor
int n = 0;
void setup() {
  // declare the ledPin as an OUTPUT:
  Serial.begin(9600);
}

void loop() {
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);
if (sensorValue > 0){
Serial.print(n);

Serial.println(": 1");

}

if (sensorValue == 0){
Serial.print(n);

Serial.println(": 0");

}
delay(100);
n++;
}
