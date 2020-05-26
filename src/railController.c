int in1 = 7;
int in2 = 5;
char in_data;
int duration; // the number of the pulses
boolean Direction; //the rotaion direction

const byte ENC_PIN_A = 2;
const byte ENC_PIN_B = 3;
byte ENC_PIN_LAST;

void setup() {

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  Serial.begin(9600); //initialize the serial port
  Encoderlnit(); // initialize the module

}

void loop() {

    if(Serial.available() > 0){

        switch(Serial.read()){  

            case '1' :  
                M1_CW(1330,255);  
                Serial.println("case 1 : Done");  
                Serial.println('1');  
                break;    

            case '2' :  
                M1_CCW(1330,255);     
                Serial.println("case 1 : Done");  
                Serial.println('A');  
                break;    

            case '3' :  
                M1_stop();    
                Serial.println("case 1 : Done");  
                Serial.println('3');  
                break;    

            default :   
                Serial.println("Err /n");
                Serial.write('n');  
                break;  
        }
    }   

    Serial.print ("Pulse : ");

    Serial.println(duration);

    in_data = Serial.read();

    Serial.print("in_data : ");

    Serial.println(in_data);

    delay(50);

}  

//a = enc , b = speed (0~255)

void M1_CW(int a, int b) {

    Serial.print("1 : turn clockwise\n");

    while(abs(duration) <= a){

        Serial.print("duration : ");
        Serial.println(duration);
        digitalWrite(in1,HIGH);
        digitalWrite(in2,LOW);
        analogWrite(6, b);      //속도제어 재료 부족

        if(Serial.read() == '0'){ //모터 회전이 없을때 루프 탈출
            Serial.print("escape");
            break;
        }

    }
    M1_stop();
    Serial.write('y');
}

 

//a = enc , b = speed (0~255)

void M1_CCW(int a, int b) {

    Serial. print("2 : turn counterclockwise\n");

    while(abs(duration) <= a){
        Serial.print("duration : ");
        Serial.println(duration);
        digitalWrite(in1, LOW);
        digitalWrite(in2, HIGH);

        analogWrite(6, b);      //속도제어 재료 부족

        if(Serial.read() == '0'){ //모터 회전이 없을때 루프 탈출
            Serial.print("escape");
            break;
        }
    }
    M1_stop();
    Serial.write('y');
}

 

void M1_stop() {

    digitalWrite(in1, LOW);
    digitalWrite(in2, LOW);
    Serial.print("3 : stop\n");

    delay(500);
    duration = 0;      

}

 

void Encoderlnit()  {
    Direction = true; // defoult ->Forwad
    pinMode(ENC_PIN_B,INPUT);
    attachInterrupt(0,wheelSpeed,CHANGE); //int.0
}

 

void wheelSpeed() {

    int Lstate = digitalRead(ENC_PIN_A);

    if((ENC_PIN_LAST == LOW) && Lstate==HIGH)
    {

        int val = digitalRead(ENC_PIN_B);

        if(val == LOW && Direction)
        {
            Direction = false; // Reverse
        }

        else if(val == HIGH && !Direction)
        {
            Direction = true; // Forward
        }

    }

    ENC_PIN_LAST = Lstate;
    
    if(!Direction) duration++;

    else duration--;

}