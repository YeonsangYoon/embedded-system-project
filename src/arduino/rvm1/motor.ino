// DC Motor 1 : rail
//a = enc , b = speed (0~255)
//int count = 0;
//int temp = 0;
//int temp1 = 0; 
void M1_CW(int b, int c)
{
    // Serial.print("1 : turn clockwise\n");
    digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
    analogWrite(analog, b);      //속도제어 재료 부족
    delay(c);

    M1_stop();
}

//a = enc , b = speed (0~255)
void M1_CCW(int b, int c) {
    // Serial.print("2 : turn counterclockwise\n");
    digitalWrite(in1, LOW);
    digitalWrite(in2, HIGH);
    analogWrite(analog, b);      
    delay(c);

    M1_stop();
}

void M1_stop()
{
    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
  // Serial.println("3 : stop");
    delay(500);
}



//===============DC Motor 2 : Sifting==============================================================
//a = enc , b = speed (0~255)
void M2_CW(int a, int b) {

    int temp = 0;
    int temp1 = 0;
    int count = 0;
    // Serial.print("1 : turn clockwise\n");
  
    while(abs(M2_duration) <= a)
    {
        // Serial.print("M2_duration : ");
        // Serial.println(M2_duration);
        digitalWrite(M2_in1,HIGH);
        digitalWrite(M2_in2,LOW);
        analogWrite(analog2, b);   
        
        delay(5);
/*
        if(Serial.read() == '0'){ //모터 회전이 없을때 루프 탈출
      // Serial.print("escape");
          break;
        }
  */
        temp = M2_duration;
        if(temp==temp1)
        {
          count++;
          if(count>2000)
              break;
        }
        else
    {
          count = 0;
    }
        temp1 = M2_duration;
    }
  // delay(c);
    M2_stop();
}

//a = enc , b = speed (0~255)
void M2_CCW(int a, int b) 
{
    int temp = 0;
    int temp1 = 0;
    int count = 0;

    digitalWrite(M2_in1, LOW);
    digitalWrite(M2_in2, HIGH);
    
    while(abs(M2_duration) <= a)
    {
        // Serial.print("M2_duration : ");
        // Serial.println(M2_duration);

        analogWrite(analog2, b);
        /*
        if(Serial.read() == '0')
        { 
            // Serial.print("escape");
            break;
        }
        */
        delay(5);

        temp = M2_duration;
        if(temp==temp1)
        {
            count++;
            if(count>00)
                break;
        }
        else
        {
            count = 0;
        }

        temp1 = M2_duration;
    }
    M2_stop();
}

void M2_stop() {
    digitalWrite(M2_in1, LOW);
    digitalWrite(M2_in2, LOW);
  // Serial.println("3 : stop");
    // delay(500);
    M2_duration = 0;      
}


//DC Motor 3 : Exit
//a = enc 
void M3_CW(int a)
{
    int temp = 0;
    int temp1 = 0;
    int count = 0;

    digitalWrite(M3_in1,HIGH);
    digitalWrite(M3_in2,LOW);
    
    while(abs(M3_duration) <= a){
        delay(5);
        temp = M3_duration;
        if(temp==temp1)
        {
            count++;
            if(count>100)
                break;
        }
        else
    {
            count = 0;
        }
        temp1 = M3_duration;
    }
    M3_stop();
}

//a = enc , b = speed (0~255)
void M3_CCW(int a)
{
    int temp = 0;
    int temp1 = 0;
    int count = 0;

    digitalWrite(M3_in1,LOW);
    digitalWrite(M3_in2,HIGH);

    while(abs(M3_duration) <= a){
         //Serial.print("M3_duration : ");
         //Serial.println(M3_duration);
         
        delay(5);
        temp = M3_duration;
        if(temp==temp1)
        {
            count++;
            if(count>100)
              break;
        }
        else
    {
            count = 0;
        }
        temp1 = M3_duration;
    }
    M3_stop();
}
void M3_stop() 
{

  digitalWrite(M3_in1, LOW);
  digitalWrite(M3_in2, LOW);
  // Serial.println("3 : stop");
  // delay(500);
  M3_duration = 0;      
}

//=====================Step Motor1 : Entrance============================================================
void stepM(int stepsPerRevolution)
{
  myStepper.step(stepsPerRevolution);
  //delay(500);
}
