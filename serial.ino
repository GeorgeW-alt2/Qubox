int sensorPin = A0;   // select the input pin for the glass diodes
int sensorValue = 0;   // variable to store the value coming from the sensor
float mappedValue = 0.0;  // variable to store the mapped float value

void setup() {
  // initialize the serial communication at 9600 baud rate:
  Serial.begin(9600);
}

void loop() {
  // read the value from the sensor:
  sensorValue = analogRead(sensorPin);

  // Map the sensor value (0-1023) to the range (0.0 - 1.0)
  mappedValue = sensorValue / 1023.0;  // This divides the value by 1023 to scale it to 0.0 to 1.0
  
  // Print the mapped float value to the serial monitor
  Serial.println(mappedValue, 4);  // Print with 4 decimal places

  
  // Add a small delay to allow for stable readings
  delay(1);
}
