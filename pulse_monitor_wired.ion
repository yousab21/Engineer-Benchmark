#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat = 0;

float beatsPerMinute;
float beatAvg;

void setup() {
  Serial.begin(115200);

  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println("MAX30102 not found");
    while (1);
  }

  particleSensor.setup(); 
  particleSensor.setPulseAmplitudeRed(0x0A); 
  particleSensor.setPulseAmplitudeGreen(0);
}

void loop() {
  long irValue = particleSensor.getIR();

  if (irValue < 50000) { 
    beatsPerMinute = 0;
    beatAvg = 0;
  } 
  else { 
    if (checkForBeat(irValue)) {
      long delta = millis() - lastBeat;
      lastBeat = millis();

      beatsPerMinute = 60 / (delta / 1000.0);

      if (beatsPerMinute < 255 && beatsPerMinute > 20) {
        rates[rateSpot++] = (byte)beatsPerMinute;
        rateSpot %= RATE_SIZE;

        int sum = 0;
        for (byte i = 0; i < RATE_SIZE; i++) sum += rates[i];
        beatAvg = sum / (float)RATE_SIZE;
      }
    }
  }

  // عرض IR + BPM + المتوسط
  Serial.print("IR: ");
  Serial.print(irValue);
  Serial.print(" | BPM: ");
  Serial.print(beatsPerMinute);
  Serial.print(" | Avg: ");
  Serial.println(beatAvg);

  
  delay(5);
}
