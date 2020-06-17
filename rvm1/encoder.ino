// 엔코더 초기화
void Encoderlnit()  {

  M2_Direction = true; // defoult ->Forwad
  M3_Direction = true; // defoult ->Forwad
  pinMode(ENC_PIN_B,INPUT);
  pinMode(ENC_PIN_B2,INPUT);

  attachInterrupt(0,wheelSpeed,CHANGE); //int.0
  attachInterrupt(1,wheelSpeed,CHANGE); //int.0
  attachInterrupt(4,wheelSpeed2,CHANGE); //int.0
  attachInterrupt(5,wheelSpeed2,CHANGE); //int.0
}

// DC M2 Encoder
void wheelSpeed() {
  int Lstate = digitalRead(ENC_PIN_A);
  
  if((ENC_PIN_LAST == LOW) && Lstate==HIGH)
  {
    int val = digitalRead(ENC_PIN_B);
    if(val == LOW && M2_Direction)
    {
      M2_Direction = false; // Reverse
    }
    else if(val == HIGH && !M2_Direction)
    {
      M2_Direction = true; // Forward
    }
  }
  ENC_PIN_LAST = Lstate;
  if(!M2_Direction) M2_duration++;
  else M2_duration--;
}

 

// DC M3 Encoder
void wheelSpeed2() {
  int Lstate = digitalRead(ENC_PIN_A2);
  if((ENC_PIN_LAST2 == LOW) && Lstate==HIGH)
  {
    int val = digitalRead(ENC_PIN_B2);
    if(val == LOW && M3_Direction)
    {
      M3_Direction = false; // Reverse
    }

    else if(val == HIGH && !M3_Direction)
    {
      M3_Direction = true; // Forward
    }
  }
  ENC_PIN_LAST2 = Lstate;
  if(!M3_Direction) M3_duration++;
  else M3_duration--;
}
