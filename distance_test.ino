
float distance=0;
 float time=0;
 const int echo=7;
 const int trig=6;
 long randomNum=0;
 float accuracy=0;
 float error=0;
 float x=0;

void distance_test(){ 
  
  Serial.begin(9600);
  pinMode(echo,INPUT);
  pinMode(trig,OUTPUT);
  randomNum=random(60,300);
  //Serial.print("rais your hand to this distance:");    // may be change it with the lid but i think serial messages is more easy for audiance
  //Serial.println(randomNum);
  //Serial.println("You have 5 seconds...");
  delay(5000);
  
 float sum=0;
 for( int i=0;i<4;i++){
 digitalWrite(trig,LOW);
 delayMicroseconds(5);
 digitalWrite(trig,HIGH);
 delayMicroseconds(10); 
 digitalWrite(trig,LOW);
 time =pulseIn(echo,HIGH,30000);
 if (time == 0) { i--; continue;}   // this was a help from my brother (claud), it return to the start of (for loop) if the sensour did not recive respond for a body
 float d=(time*0.0343)/2;
 sum+=d;
 delay(50);
  }
  distance=sum/4;
  error=randomNum-distance;
  x=abs(error);   // abs()>>>>>>to give us the absolut value
  accuracy= (1.0 - (x / randomNum)) * 100;
  if (accuracy < 0) acuracy = 0; // if your so dumm that you have accuracy in negative it will give you zero

  //Serial.print("accuracy=");
  //Serial.print(accuracy);
  //Serial.println("%");
  //delay(100);
}

void setup() {
  distance_test();
} 

void loop(){
}
