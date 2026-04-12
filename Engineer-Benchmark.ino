#include <HX711.h>
#include <MPU6050.h>
#include <Wire.h>

// Force Test pins
#define FORCE_DAT 4
#define FORCE_CLK 5

// Distance Test pins
#define DIST_TRIG 6
#define DIST_ECHO 7

// Reflex Test pins
#define REFLEX_TRIG      2
#define REFLEX_ECHO      3
#define REFLEX_RED_LED   11
#define REFLEX_GREEN_LED 12

// Time Perception Test pins
#define TIME_TOUCH 8

//Agnle Perception Test pins
//this sensors works via i2c and those pins are hard coded into
//the library those comments are just for us when we assemble the project
// SDA -> A4 
// SCL -> A5

//===============================================================

void forceTest(){
  HX711 forceSensor;
  const int calibrationFactorNewtons = 6700;

  forceSensor.begin(FORCE_DAT, FORCE_CLK);
  forceSensor.tare();
  forceSensor.set_scale(calibrationFactorNewtons);

  randomSeed(analogRead(0));
  int randomNumber = random(0, 10);
  Serial.println(randomNumber);
  delay(3000);

  float total = 0;
  for (int i = 0; i < 5; i++){
    total += forceSensor.get_units(10);
    delay(1000);
  }
  float averageReading = total / 5;
  float averageError = abs(averageReading - randomNumber);
  Serial.println(averageError);
}

//===============================================================

void distanceTest(){
  randomSeed(analogRead(0));
  int randomNum = random(10, 80);
  Serial.println(randomNum);
  delay(3000);

  float sum = 0;
  for (int i = 0; i < 5; i++){
    digitalWrite(DIST_TRIG, LOW);
    delayMicroseconds(5);
    digitalWrite(DIST_TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(DIST_TRIG, LOW);
    float time = pulseIn(DIST_ECHO, HIGH);
    if (time == 0) { i--; continue; }
    float d = (time * 0.0343) / 2;
    sum += d;
    delay(1000);
  }
  float distance = sum / 5;
  float relativeError = abs((randomNum - distance) / randomNum);
  Serial.println(relativeError);
}

//===============================================================

long getReflexDistance() {
  digitalWrite(REFLEX_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(REFLEX_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(REFLEX_TRIG, LOW);
  long duration = pulseIn(REFLEX_ECHO, HIGH, 30000);
  if (duration == 0) return 999;
  return duration * 0.034 / 2;
}

void reflexTest() {
  Serial.println(0);
  delay(3000);

  while (getReflexDistance() > 5 || getReflexDistance() == 0);

  for (int i = 0; i < 3; i++) {
    digitalWrite(REFLEX_RED_LED, HIGH);
    delay(700);
    digitalWrite(REFLEX_RED_LED, LOW);
    delay(700);
  }

  randomSeed(analogRead(0));
  delay(random(1000, 4000));
  digitalWrite(REFLEX_GREEN_LED, HIGH);
  delay(50);

  long startTime = millis();
  int confirmed = 0;
  while (confirmed < 3) {
    if (getReflexDistance() > 15) {
      confirmed++;
    } else {
      confirmed = 0;
    }
    delay(5);
  }
  digitalWrite(REFLEX_GREEN_LED, LOW);
  long reflexTime = (millis() - startTime) + 50;
  Serial.println(reflexTime);
}

//===============================================================

void timePerceptionTest() {
  randomSeed(analogRead(0));
  int target = random(5, 15);
  Serial.println(target);
  delay(3000);

  long gameStartTime = millis();
  while (digitalRead(TIME_TOUCH) == LOW);
  long userTouchTime = millis();

  float durationInSeconds = (userTouchTime - gameStartTime) / 1000.0;
  float difference = abs(durationInSeconds - target);
  float errorPercent = (difference / target) * 100.0;
  Serial.println(errorPercent);
}

//===============================================================

void anglePerceptionTest(){
  randomSeed(analogRead(0));
  bool positive = random(0, 2);
  int randomAngle;
  if (positive) {
    randomAngle = random(10, 80);
  } else {
    randomAngle = random(-80, -10);
  }

  Serial.println(randomAngle);
  delay(3000);

  MPU6050 mpu;
  Wire.begin();
  mpu.initialize();

  float totalError = 0;
  for (int i = 0; i < 5; i++) {
    int16_t ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    float angle = atan2((float)ax, (float)az) * 180.0 / PI;
    float error = abs(angle - randomAngle);
    totalError += error;
    delay(1000);
  }

  float avgError = totalError / 5;
  float errorPercent = (avgError / abs(randomAngle)) * 100.0;
  Serial.println(errorPercent);
}

//===============================================================

void setup() {
  Serial.begin(9600);

  pinMode(FORCE_DAT,        INPUT);
  pinMode(FORCE_CLK,        OUTPUT);

  pinMode(DIST_TRIG,        OUTPUT);
  pinMode(DIST_ECHO,        INPUT);

  pinMode(REFLEX_TRIG,      OUTPUT);
  pinMode(REFLEX_ECHO,      INPUT);
  pinMode(REFLEX_RED_LED,   OUTPUT);
  pinMode(REFLEX_GREEN_LED, OUTPUT);

  pinMode(TIME_TOUCH,       INPUT);
}

void loop() {
  if (Serial.available()) {
    String request = Serial.readStringUntil('\n');
    request.trim();
    if      (request == "FORCE_TEST")    forceTest();
    else if (request == "DISTANCE_TEST") distanceTest();
    else if (request == "REFLEX_TEST")   reflexTest();
    else if (request == "TIME_TEST")     timePerceptionTest();
    else if (request == "ANGLE_TEST")    anglePerceptionTest();
    else                                 Serial.println("BAD_REQUEST");
  }
}
