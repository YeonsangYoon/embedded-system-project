#include <Stepper.h>

//DC M1 핀넘버
int in1 = 5;
int in2 = 4;
int analog = 6;

//DC M2 핀넘버
int M2_in1 = 11;
int M2_in2 = 12;
int analog2 =13;

//DC M2 엔코더 핀
const byte ENC_PIN_A = 2;
const byte ENC_PIN_B = 53;
byte ENC_PIN_LAST;

int M2_duration; // the number of the pulses
boolean M2_Direction; //the rotaion M2_Direction

//============ 분별기 =============
//DC M3 핀넘버
int M3_in1 = 52;
int M3_in2 = 50;
int analog3 =7;

//DC M3 엔코더 핀
const byte ENC_PIN_A2 = 3;
const byte ENC_PIN_B2 = 51;
byte ENC_PIN_LAST2;

int M3_duration; // the number of the pulses
boolean M3_Direction; //the rotaion M2_Direction


//=================PID제어 테스트==========
// motor control pin
const int motorDirPin = 52; // L298 Input 1
const int motorPWMPin = 50; // L298 Input 2

// encoder pin
const int encoderPinA = 2;
const int encoderPinB = 3;

int encoderPos = 0;

const float ratio = 360./360.;
float Kp = 30;
float targetDeg = 360;
 
void doEncoderA(){
	encoderPos += (digitalRead(encoderPinA)==digitalRead(encoderPinB))?1:-1;
  	}

void doEncoderB(){
  	encoderPos += (digitalRead(encoderPinA)==digitalRead(encoderPinB))?-1:1;
  	}

void doMotor(bool dir, int vel){
  	digitalWrite(motorDirPin, dir);
  	analogWrite(motorPWMPin, dir?(255 - vel):vel);
}


char in_data; //case Number 

// 2048:한바퀴(360도), 1024:반바퀴(180도)...
const int stepsPerRevolution = 2048; 

// 모터 드라이브에 연결된 핀 IN4, IN2, IN3, IN1
Stepper myStepper(stepsPerRevolution,49,48,47,46);   

//============SETUP======================================

void setup() {
  	pinMode(in1, OUTPUT);
  	pinMode(in2, OUTPUT);
  	Serial.begin(9600); //initialize the serial port
  	Encoderlnit(); // initialize the module

  	myStepper.setSpeed(15);
}

//============LOOP========================================
void loop() {
stepM( stepsPerRevolution*(2.5));
stepM(stepsPerRevolution*(-2.5));

/*
 	float motorDeg = float(encoderPos)*ratio;
 	float error = targetDeg - motorDeg;
 	float control = Kp*error;

 	doMotor( (control>=0)?HIGH:LOW, min(abs(control), 255));
 	Serial.print("encoderPos : ");
 	Serial.print(encoderPos);
 	Serial.print("   motorDeg : ");
 	Serial.print(float(encoderPos)*ratio);
 	Serial.print("   error : ");
 	Serial.print(error);
 	Serial.print("    control : ");
 	Serial.print(control);
 	Serial.print("    motorVel : ");
 	Serial.println(min(abs(control), 255));
*/

if(Serial.available() > 0){

  	in_data = Serial.read();
  	Serial.print("in_data : ");
  	Serial.println(in_data);
  	delay(50);

  	switch(in_data){  

  	case '1' :
//  	M3_CCW(360,70);
    	M3_getback(30, 100, 300);
//  	stepM(stepsPerRevolution);
//  	Serial.println("case 1 : Done");
//  	Serial.println('1');
    	Flush();
    	break;

  	case '2' :
    	M3_CCW(1330,222); 
//  	Serial.println("case 1 : Done");
//  	Serial.println('A');
    	Flush();
    	break;

    

  	case '3' :
    	M2_stop();
//  	Serial.println("case 1 : Done");
//  	Serial.println('3');
    	Flush();
    	break;

  	default :
    	Serial.println(in_data);
    	Serial.println("Err /n");
  		break;
  	}
}

  	Serial.print ("Pulse : ");
  	Serial.println(M3_duration);
}  

 

 

//===============DC Motor 1 : rail==============================================================

//a = enc , b = speed (0~255)

void M1_CW(int a, int b, int c) {

  	Serial.print("1 : turn clockwise\n");
    
	digitalWrite(in1,HIGH);
    digitalWrite(in2,LOW);
    analogWrite(analog, b);      //속도제어 재료 부족
    delay(c);

  	M1_stop();

  	Serial.println('y');

}

 

//a = enc , b = speed (0~255)

void M1_CCW(int a, int b, int c) {

  	Serial. print("2 : turn counterclockwise\n");

	digitalWrite(in1, LOW)	
	digitalWrite(in2, HIGH)	
	analogWrite(analog, b);     	
	delay(c);

  	M1_stop();

  	Serial.println('y');
}

 

void M1_stop() {

  	digitalWrite(in1, LOW);
  	digitalWrite(in2, LOW);

	// Serial.println("3 : stop");

  	delay(500);
}

//===============DC Motor 2 : Exit==============================================================

 

//a = enc , b = speed (0~255)

void M2_CW(int a, int b) {

  	Serial.print("1 : turn clockwise\n");

	while(abs(M2_duration) <= a){
	  	Serial.print("M2_duration : ");
	  	Serial.println(M2_duration);

	  	digitalWrite(M2_in1,HIGH);
	  	digitalWrite(M2_in2,LOW);
	  	analogWrite(analog2, b);      //속도제어 재료 부족
		if(Serial.read() == '0'){ //모터 회전이 없을때 루프 탈출
	  		Serial.print("escape");
	  		break;
		}

	 	// delay(c);

	}
  	M2_stop();
  	Serial.println('y');
}

 

//a = enc , b = speed (0~255)

void M2_CCW(int a, int b) {

  	Serial. print("2 : turn counterclockwise\n");

	while(abs(M2_duration) <= a){
		Serial.print("M2_duration : ");
		Serial.println(M2_duration);
		
		digitalWrite(M2_in1, LOW);
		digitalWrite(M2_in2, HIGH);
		analogWrite(analog2, b);

		if(Serial.read() == '0'){ 
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

	// Serial.println("3 : stop");

  	delay(500);

  	M2_duration = 0;      
}

 

//a : enc, b : speed, c : delay

void M2_getback(int a, int b, int c){
  	M2_CW(a, b);
  	delay(c);
  	M2_CCW(a, b);
}

 

//===============DC Motor 3 : Sifting ==============================================================

 

//a = enc , b = speed (0~255)

void M3_CW(int a, int b) {

	Serial.print("1 : turn clockwise\n");	
	
	while(abs(M3_duration) <= a){	
	    Serial.print("M3_duration : ");	
	    Serial.println(M3_duration);	

	    digitalWrite(M3_in1,HIGH);	
	    digitalWrite(M3_in2,LOW);	
	    analogWrite(analog3, b);      //속도제어 재료 부족	
	  	
		if(Serial.read() == '0'){ //모터 회전이 없을때 루프 탈출	
	    	Serial.print("escape");	
	    	break;	
	  	}
 	// delay(c);
  	}
  M3_stop();
  Serial.println('y');
}

 

//a = enc , b = speed (0~255)

void M3_CCW(int a, int b) {
  	Serial. print("3 : turn counterclockwise\n");
    
	while(abs(M3_duration) <= a){
      	Serial.print("M3_duration : ");
      	Serial.println(M3_duration);

      	digitalWrite(M3_in1, LOW);
      	digitalWrite(M3_in2, HIGH);
      	analogWrite(analog3, b);

      	if(Serial.read() == '0'){ 
        	Serial.print("escape");
      		break;
      	}
  	}
  	M3_stop();
  	Serial.println('y');
}

void M3_stop() {
  	digitalWrite(M3_in1, LOW);
  	digitalWrite(M3_in2, LOW);

	// Serial.println("3 : stop");
  	delay(500);
  	M3_duration = 0;      
}

 

//a : enc, b : speed, c : delay

void M3_getback(int a, int b, int c){
  	M3_CW(a, b);
  	delay(c);
  	M3_CCW(a, b);
}

//============================DC M2 Encoder====================================

void Encoderlnit()  {
  	M2_Direction = true; // defoult ->Forwad
  	M3_Direction = true; // defoult ->Forwad

  	pinMode(ENC_PIN_B,INPUT);
  	pinMode(ENC_PIN_B2,INPUT);
  	attachInterrupt(0,wheelSpeed,CHANGE); //int.0
  	attachInterrupt(1,wheelSpeed2,CHANGE); //int.0
}

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

//============================DC M3 Encoder====================================

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

 

//=====================Step Motor1 : Entrance============================================================

void stepM(int stepsPerRevolution){
  myStepper.step(stepsPerRevolution);
  delay(500);
}

 

void Flush(){
  	if(Serial.available() > 0){
        //남은 incoming 버퍼 지우기
      	while(Serial.available() > 0){
        	Serial.read();
      	}
  	}
}