//Qubox - 2024
#include "pitches.h"
const int MAX_ITEMS = 8;
int n = 0;
int varX = 0;
int varY = 0;

const int total_binary_numbers = 2;
int itemCount = total_binary_numbers;      // Tracks the number of items added

String str = "";
String input;
// notes in the melody:
int melody[] = {
  NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
};

// note durations: 4 = quarter note, 8 = eighth note, etc.:
int noteDurations[] = {
  4, 8, 8, 4, 4, 4, 4, 4
};

const int checkPin = 10;
const int delayTimePin = A4;    // Potentiometer for delay time
const int LDR = A0;
const int delayedOutputPin = A3;
const int buzzerPin = 9;        // Digital output pin for buzzer

const int powerPin = 12;        // Digital output pin for laser diode

float delayLine[200];           // Maximum delay line size
int writeIndex = 0;             // Write index for delay line
int maxDelaySamples = 50;       // Max delay samples
int sampleRate = 50;            // Default sample rate
int delayTime = 1;              // Default delay time in milliseconds
int value = 15;
int inputint = 0;
int inputint2 = 0;
unsigned long unequalStartTime = 0; // Start time for proper time duration
unsigned long properTimeDuration = 0; // Measured proper time duration
bool unequalActive = false;     // Track if unequal period is active

// Define an array of 4 elements to hold random binary values
int numbers[total_binary_numbers];  

void setup() {
  // Seed the random number generator with an analog reading
  randomSeed(analogRead(A2));  
  varY = random(0, 20);
  Serial.begin(9600);
  pinMode(powerPin, OUTPUT); 
  pinMode(buzzerPin, OUTPUT);
  pinMode(checkPin, OUTPUT); 
  pinMode(LDR, OUTPUT); 

  digitalWrite(powerPin, HIGH);
  
  Serial.println("Enter range e.g. 1,4 or 5,8 or type 'show' to show hidden variable: ");

  // Generate random binary values for the numbers array
  for (int i = 0; i < total_binary_numbers ; i++) {
    numbers[i] = random(0, 2);  // Each element will be either 0 or 1
  }
}
void addItem(int item) {
    if (itemCount < MAX_ITEMS) {
        numbers[itemCount] = item;
        itemCount++;
    } else {
        Serial.println("Array is full!");
    }
}
void loop() {
  // Read values from potentiometers
  //Serial.print("Code input: ");

  String inputStr = Serial.readStringUntil('\n');  // Read input as a String until '.'
  int commaIndex = inputStr.indexOf(',');  // Find the comma in the input
  if (inputStr == "show"){
    Serial.println(varY);

  }
  // Extract the first and second integers from the input
  if (inputStr.length() > 0){
  int inputint = inputStr.substring(0, commaIndex).toInt();  // Get the first number before the comma
  int inputint2 = inputStr.substring(commaIndex + 1).toInt();  // Get the second number after the comma

  // Print the results
  Serial.print("First number: ");
  Serial.println(inputint);
  Serial.print("Second number: ");
  Serial.println(inputint2);
  varX = random(inputint, inputint2); //insert range to perform quantum search
}
  int range = numbers[n];
  switch (range) { //logical qubit
    case 0:
      
      break;
    case 1:
      if (varX == varY){
      delayTime = map(analogRead(delayTimePin), 0, 1023, 1000, 1);

      }
      break;
  }

  // Update the maxDelaySamples based on the delay time
  maxDelaySamples = (sampleRate * delayTime) / 1000;

  // Read from analog input (e.g., LDR sensor)
  int input = analogRead(LDR);

  // Get the delayed value
  float delayedValue = delayLine[writeIndex];

  // Output the delayed value to analog output (PWM)
  analogWrite(delayedOutputPin, delayedValue);

  // Store the new sample in the delay line
  delayLine[writeIndex] = input;

  // Increment and wrap the write index
  writeIndex = (writeIndex + 1) % maxDelaySamples;

  // Check if input and delayed values are unequal
  if (input > value && delayedValue < value && input != delayedValue && delayedValue != 0 && input != 0) {
    if (input > delayedValue + 5 || input < delayedValue - 5) {
      if (!unequalActive) { // If this is the start of an unequal period
        unequalStartTime = millis();
        unequalActive = true;
      }
      tone(buzzerPin, melody[0], 10);
      digitalWrite(checkPin, HIGH);
    }
  } else {
    if (unequalActive) { // If unequal period just ended
      properTimeDuration = millis() - unequalStartTime;
      unequalActive = false;
    }
    noTone(buzzerPin);
    digitalWrite(checkPin, LOW);
  }
  if (digitalRead(checkPin) == 1){
    n++;
    Serial.println(varY);

  }
/*
  // Print results to Serial Monitor
  Serial.print(" Input Value: ");
  Serial.print(input);
  Serial.print(" - Buzzer Signal: ");
  Serial.print(digitalRead(checkPin));
  

  Serial.print(" Delayed Output: ");
  Serial.print(delayedValue);
  Serial.print(" Sample Rate: ");
  Serial.print(sampleRate);
  Serial.print(" Hz");

  // Display proper time duration when unequal period ends
  if (!unequalActive && properTimeDuration > 0) {
    Serial.print(" - Proper Time Duration: ");
    Serial.print(properTimeDuration);
    Serial.print(" ms");
  }

  Serial.print(str);
  */
/*
  // Print the array values if n >= 3
  if (n == total_binary_numbers ) {
    Serial.print(" Original code: ");
    for (int i = 0; i < sizeof(numbers) / sizeof(numbers[0]); i++) {
      Serial.print(numbers[i]);
      if (i < sizeof(numbers) / sizeof(numbers[0]) - 1) {
        Serial.print(", ");  
      }
    }

  }
*/
  delay(1);
}
