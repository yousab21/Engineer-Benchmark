const int st1_trigPin = 2;
const int st1_echoPin = 3;
const int st1_redLed  = 11;
const int st1_greenLed = 12;

bool stationDone = false;
void setup() {
  Serial.begin(9600);
  pinMode(st1_trigPin, OUTPUT);
  pinMode(st1_echoPin, INPUT);
  pinMode(st1_redLed, OUTPUT);
  pinMode(st1_greenLed, OUTPUT);
  
  randomSeed(analogRead(0)); 

  Serial.println("Station_1 Ready :)");
}

void loop() {
  if (stationDone == false){
  long result = runStation1();
  Serial.print("Reflex Time: ");
  Serial.print(result);
  Serial.println(" ms");
  stationDone = true;
  Serial.print("STATION_1 FINISHED");
  }
}
long runStation1()
 {
  Serial.println(" PLEASE_PLACE_HAND_ON_SENSOR :)");
  while (getSt1Distance() > 5 || getSt1Distance() == 0);

  for (int i = 0; i < 3; i++) {
    digitalWrite(st1_redLed, HIGH); 
    delay(700);
    digitalWrite(st1_redLed, LOW);  
    delay(700);
  }
  delay(random(1000, 4000)); 
  digitalWrite(st1_greenLed, HIGH);
  delay(50); 
  
  long startTime = millis();

  int ta2ked_el3ad = 0;
  while (ta2ked_el3ad < 3) {
    if (getSt1Distance() > 15) { 
      ta2ked_el3ad++;
    } else {
      ta2ked_el3ad = 0; 
    }
    delay(5);
  }

  digitalWrite(st1_greenLed, LOW);
  long reflexTime = (millis() - startTime) + 50;
  return reflexTime;
}
long getSt1Distance() {
  digitalWrite(st1_trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(st1_trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(st1_trigPin, LOW);
  long duration = pulseIn(st1_echoPin, HIGH, 30000); 
  if (duration == 0) return 999;
  return duration * 0.034 / 2;
}
