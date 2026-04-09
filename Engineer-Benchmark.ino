#include<HX711.h>
void forceTest(){
  const int DAT = 4;
  const int CLK = 5;
  const int calibrationFactorNewtons = 6700;
  const int calibrationFactorGrams = 64;
  HX711 forceSensor;
  //callabration 
  forceSensor.begin(DAT, CLK);
  forceSensor.tare();
  forceSensor.set_scale(calibrationFactorNewtons);
  //get the random number of numtons to start the test and send it to the script
  int randomNumber = random(0, 10);
  Serial.println(randomNumber);
  delay(3000);
  //sensor takes 5 earding and gets the average for it to be fair
  float total = 0;
  float relativeError = 0;
  for (int i = 0 ; i< 5 ; i++){
    total += forceSensor.get_units(10);
    relativeError = total - randomNumber;
    delay(1000);
  }
  float averageError = abs(relativeError/5);
  //send the error percentage to the script
  Serial.println(averageError);
}
//===============================================================
void distanceTest(){ 
 
float distance=0;
 float time=0;
 const int echo=7;
 const int trig=6;
 int randomNum=0;
 float accuracy=0;
 float error=0;
 float x=0;
 //setup
  pinMode(echo,INPUT);
  pinMode(trig,OUTPUT);
  //chooses a raandom number and sends it to the script
  randomNum=random(10,80);
  Serial.println(randomNum);
  delay(3);
  
 float sum=0;
 for( int i=0;i<5;i++){
  //callabration
 digitalWrite(trig,LOW);
 delayMicroseconds(5);
 digitalWrite(trig,HIGH);
 delayMicroseconds(10); 
 digitalWrite(trig,LOW);
 //distance mesurement
 time =pulseIn(echo,HIGH);
 if (time == 0) { i--; continue;}   // this was a help from my brother (claud), it return to the start of (for loop) if the sensour did not recive respond for a body
 float d=(time*0.0343)/2;
 sum+=d;
 delay(1000);
  }
  distance=sum/5;
  error=randomNum-distance;
  float relativeError = error / randomNum;
  x=abs(relativeError);   // abs()>>>>>>to give us the absolut value
  Serial.println(x);
  //this is kinda cool but we want to always send the error percentageto the script not acuracy :(
  //ill keep it in the code tho as recognition of your work <3
  //accuracy= (1.0 - (x / randomNum)) * 100;
  //if (accuracy < 0) acuracy = 0; // if your so dumm that you have accuracy in negative it will give you zero
} 
//======================================
long getSt1Distance() {
  const int st1_trigPin = 2;
  const int st1_echoPin = 3;
  digitalWrite(st1_trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(st1_trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(st1_trigPin, LOW);
  long duration = pulseIn(st1_echoPin, HIGH, 30000);
  if (duration == 0) return 999;
  return duration * 0.034 / 2;
}
void reflexTest() {
  const int st1_trigPin = 2;
  const int st1_echoPin = 3;
  const int st1_redLed  = 11;
  const int st1_greenLed = 12;
  
  pinMode(st1_trigPin, OUTPUT);
  pinMode(st1_echoPin, INPUT);
  pinMode(st1_redLed, OUTPUT);
  pinMode(st1_greenLed, OUTPUT);
  Serial.println(0);  // random number slot — no target for reflex
  delay(3); //wait for the user to read instructions
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
  Serial.println(reflexTime);
}
void setup() {
  Serial.begin(9600);
}
void loop() {
      if (Serial.available()) {
        String request = Serial.readStringUntil('\n');
        request.trim();
        if (request == "FORCE_TEST") {
            forceTest();
        } else if (request == "DISTANCE_TEST") {
            distanceTest();       // future test
        }
        else if(request == "REFLEX_TEST"){
            reflexTest();
        }else {
            Serial.println("BAD_REQUEST");
        }
    }
    // does absolutely nothing until a request arrives
}
