#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"

MAX30105 particleSensor;

const byte RATE_SIZE = 4;
byte rates[RATE_SIZE];
byte rateSpot = 0;
long lastBeat  = 0;
float beatsPerMinute;
float beatAvg;

// ── state ─────────────────────────────────────────────────
enum State { IDLE, BASELINE, TRIAL };
State state = IDLE;

float baselineBPM  = 0;
float peakBPM      = 0;

const int BASELINE_SAMPLES = 10;
int   baselineCount = 0;
float baselineAccum = 0;

// ─────────────────────────────────────────────────────────
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

// ─────────────────────────────────────────────────────────
void loop() {
  // ── sensor reading (your original code) ────────────────
  long irValue = particleSensor.getIR();

  if (irValue < 50000) {
    beatsPerMinute = 0;
    beatAvg        = 0;
  } else {
    if (checkForBeat(irValue)) {
      long delta     = millis() - lastBeat;
      lastBeat       = millis();
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

  // ── state machine ───────────────────────────────────────
  if (state == BASELINE && beatAvg > 0) {
    baselineAccum += beatAvg;
    baselineCount++;
    if (baselineCount >= BASELINE_SAMPLES) {
      baselineBPM = baselineAccum / BASELINE_SAMPLES;
      peakBPM     = baselineBPM;
      state       = TRIAL;
      Serial.println("READY");
    }
  } else if (state == TRIAL) {
    if (beatAvg > peakBPM) peakBPM = beatAvg;
  }

  // ── serial commands ─────────────────────────────────────
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "START") {
      baselineBPM   = 0; peakBPM = 0;
      baselineAccum = 0; baselineCount = 0;
      for (byte i = 0; i < RATE_SIZE; i++) rates[i] = 0;
      state = BASELINE;
      Serial.println("BASELINE_COLLECTING");

    } else if (cmd == "STOP") {
      if (state == TRIAL && baselineBPM > 0) {
        float pct = ((peakBPM - baselineBPM) / baselineBPM) * 100.0;
        Serial.println(pct);
      } else {
        Serial.println("ERR:NO_BASELINE");
      }
      state = IDLE;
    }
  }

  delay(5);
}
