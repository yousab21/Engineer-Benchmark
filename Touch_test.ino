const int touchPin = 4;
// const int buzzerPin = 5;

int targetSeconds = 0;
float durationInSeconds = 0;
float difference = 0;
float absDiff = 0;     

void touch_test() {
  randomSeed(analogRead(0));
  Serial.println("--- FOCUS ON YOUR TIME :) ---");
  delay(1000);

  targetSeconds = random(5, 15); 
  
  Serial.println("\n=======================================");
  Serial.print("YOUR MISSION: Count [ ");
  Serial.print(targetSeconds);
  Serial.println(" ] Seconds in your head.");
  Serial.println("Wait for the signal...");
  delay(2000); 

  for (int i = 3; i > 0; i--) {
    Serial.print(i); Serial.println("...");
    // tone(buzzerPin, 1000, 100);
    delay(1000);
  }

  Serial.println(">>> GO! GO! GO! <<<");
  // tone(buzzerPin, 1500, 500);
  
  long gameStartTime = millis(); 

  while (digitalRead(touchPin) == LOW) {
  }

  long userTouchTime = millis();
  durationInSeconds = (userTouchTime - gameStartTime) / 1000.0;
  difference = durationInSeconds - targetSeconds;
  absDiff = abs(difference);

  Serial.println("\n[ FINISHED! ]");
  Serial.print("Target   : ");
  Serial.print(targetSeconds);
  Serial.println(".00s");
  Serial.print("Your Time: ");
  Serial.print(durationInSeconds);
  Serial.println("s");
  
  Serial.print("Accuracy : ");
  if (difference >= 0) Serial.print("+"); 
  Serial.print(difference);
  Serial.println("s");

  if (absDiff < 0.15) {
    Serial.println("RANK: TIME MASTER (  عالمي! 👑)");
    // tone(buzzerPin, 2000, 1000);
  } else if (absDiff < 0.4) {
    Serial.println("RANK: SNIPER (: قريب جداً");
  } else if (absDiff < 0.8) {
    Serial.println("RANK: NOT BAD ( شغال )");
  } else {
    Serial.println("RANK: BAD ( صحي النوم ) ");
    // tone(buzzerPin, 200, 500);
  }

  Serial.println("=======================================");
  Serial.println("GAME OVER. Press 'RESET' button on Arduino to play again.");
}

void setup() {
  Serial.begin(9600);
  pinMode(touchPin, INPUT);
  // pinMode(buzzerPin, OUTPUT);
  touch_test();
}

void loop() {
}
