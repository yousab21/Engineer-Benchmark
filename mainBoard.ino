#include<HX711.h>


void forcePerception(){
  const int DAT = 4;
  const int CLK = 5;
  const int calibrationFactorNewtons = 6700;
  const int calibrationFactorGrams = 64;
  HX711 forceSensor;
  //callabration 
  forceSensor.begin(DAT, CLK);
  forceSensor.tare();
  forceSensor.set_scale(calibrationFactorNewtons);

  //get the random number of numtons to start the test
  int randomNumber = random(0, 10);

  //some code to declare that the test began (lesa han4oof hykoon eh fi el 8aleb led aw buzzer)

  //sensor takes 5 earding and gets the average for it to be fair
  float total = 0;
  for (int i = 0 ; i< 5 ; i++){
    total += forceSensor.get_units(10);
    delay(100);
  }
  float average = total/5;
  float error = average - randomNumber;

  Serial.print(error);
  Serial.print(" ,");
}

void setup() {
  Serial.begin(9600);
//testing (hane3mel fi el a5er hub function te handle el calls kolaha)
  forcePerception();
}

void loop() {
}
