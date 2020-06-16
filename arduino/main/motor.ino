// DC Motor 1 : rail
//a = enc , b = speed (0~255)
void M1_CW(int b, int c)
{
  Serial.print("1 : turn clockwise\n");
  digitalWrite(in1,HIGH);
  digitalWrite(in2,LOW);
  analogWrite(analog, b);      //속도제어 재료 부족
  delay(c);

  M1_stop();
  Serial.println('y');
}

//a = enc , b = speed (0~255)
void M1_CCW( int b, int c) {
  Serial. print("2 : turn counterclockwise\n");
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(analog, b);      
  delay(c);

  M1_stop();
  Serial.println('y');
}

void M1_stop()
{
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
//  Serial.println("3 : stop");
  delay(500);
}



//===============DC Motor 2 : Sifting==============================================================
//a = enc , b = speed (0~255)
void M2_CW(int a, int b) {
  Serial.print("1 : turn clockwise\n");
  while(abs(M2_duration) <= a)
  {
    Serial.print("M2_duration : ");
    Serial.println(M2_duration);
    digitalWrite(M2_in1,HIGH);
    digitalWrite(M2_in2,LOW);
    analogWrite(analog2, b);      
    if(Serial.read() == '0'){ //모터 회전이 없을때 루프 탈출
      Serial.print("escape");
      break;
    }
 //  delay(c);
  }
  M2_stop();
  Serial.println('y');
}

//a = enc , b = speed (0~255)
void M2_CCW(int a, int b) 
{
  Serial. print("2 : turn counterclockwise\n");
  while(abs(M2_duration) <= a)
  {
    Serial.print("M2_duration : ");
    Serial.println(M2_duration);

    digitalWrite(M2_in1, LOW);
    digitalWrite(M2_in2, HIGH);
    analogWrite(analog2, b);      
    if(Serial.read() == '0')
    { 
      Serial.print("escape");
      break;
    }
  }
  M2_stop();
  Serial.println('y');
}

void M2_stop() {
  digitalWrite(M2_in1, LOW);
  digitalWrite(M2_in2, LOW);
//  Serial.println("3 : stop");
  delay(500);
  M2_duration = 0;      
}


//DC Motor 3 : Exit
//a = enc 
void M3_CW(int a)
{
  Serial.print("1 : turn clockwise\n");
  while(abs(M3_duration) <= a){
    Serial.print("M3_duration : ");
    Serial.println(M3_duration);
    digitalWrite(M3_in1,HIGH);
    digitalWrite(M3_in2,LOW);
    if(Serial.read() == '0'){ //모터 회전이 없을때 루프 탈출
      Serial.print("escape");
      break;
    }
 //  delay(c);
  }
  M3_stop();
  Serial.println('y');
}

//a = enc , b = speed (0~255)
void M3_CCW(int a) 
{
  Serial. print("3 : turn counterclockwise\n");
  while(abs(M3_duration) <= a)
  {
    digitalWrite(M3_in1, LOW);
    digitalWrite(M3_in2, HIGH);   
    if(Serial.read() == '0'){ 
      Serial.print("escape");
      break;
    }
  }
  M3_stop();
  Serial.println('y');
}

void M3_stop() 
{
  digitalWrite(M3_in1, LOW);
  digitalWrite(M3_in2, LOW);
//  Serial.println("3 : stop");
  delay(500);
  M3_duration = 0;      
}

//=====================Step Motor1 : Entrance============================================================
void stepM(int stepsPerRevolution)
{
  myStepper.step(stepsPerRevolution);
  delay(500);
}
