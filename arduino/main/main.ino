/*
 * 프로그램 내용 : 
 *              RVM (Reverse Vending Machine) - 재활용품(캔, 패트병)을
 *              넣으면 물체인식 알고리즘(Yolo)를 사용하여 분류를 한다.
 *              
 *              아두이노는 라즈베리파이로부터 신호를 받아서 상황에 맞게 모터를
 *              구동시킨다. 아두이노 전원은 12V 3A를 사용하였고 총 4개의 모터를 제어한다.
 *              
 *              스탭모터 - 렉피니언과 연결하여 로드셀이 장착되어 있는 밑판을 들어올리고 내린다.
 *              DC모터1 - 물건 전달에 사용되는 레일의 샤프를 회전시킨다.
 *              DC모터2 - 물건이 재활용품(캔)일때, 렉피니언을 통하여 물건을 밀어준다.
 *              DC모터3 - 물건이 재활용품(패트병)일때, 가림판을 회전시켜서
 *                       물건이 지나갈 수 있도록 길을 열어준다.
 */

#include <Stepper.h>

// 핀 번호
//DC M1 핀넘버
#define in1     5
#define in2     4
#define analog  6

//DC M2 핀넘버
#define M2_in1  13
#define M2_in2  12
#define analog2 11

//DC M2 엔코더 핀
const byte ENC_PIN_A = 2;
const byte ENC_PIN_B = 3;
byte ENC_PIN_LAST;

//DC M3 핀넘버
#define M3_in1  10   //50
#define M3_in2  9    //52

//DC M3 엔코더 핀
const byte ENC_PIN_A2 = 18;
const byte ENC_PIN_B2 = 19;
byte ENC_PIN_LAST2;

int M2_duration; // the number of the pulses
boolean M2_Direction; //the rotaion M2_Direction

int M3_duration; // the number of the pulses
boolean M3_Direction; //the rotaion M2_Direction

char in_data; //case Number

 

// 2048:한바퀴(360도), 1024:반바퀴(180도)...

const int stepsPerRevolution = 2048; 

// 모터 드라이브에 연결된 핀 IN4, IN2, IN3, IN1

Stepper myStepper(stepsPerRevolution,49,48,47,46);   

void setup() {

  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(M2_in1, OUTPUT);
  pinMode(M2_in2, OUTPUT);
  pinMode(M3_in1, OUTPUT);
  pinMode(M3_in2, OUTPUT);
  
  Encoderlnit(); // initialize the module
  myStepper.setSpeed(12); 

  Serial.begin(9600); //initialize the serial port
}

void loop()
{
  Serial.print("M2_en : ");
  Serial.print(M2_duration);
  Serial.print("\tM3_en : ");
  Serial.println(M3_duration);
  delay(100);
  
  if(Serial.available() > 0)
  {
    Serial.print("M2_en : ");
    Serial.println(M2_duration);
    in_data = Serial.read();
  
    Serial.print("in_data : ");
    Serial.println(in_data);
  
    delay(50);

    switch(in_data)
    {

      case '1' :
    //  stepM(stepsPerRevolution*1);
    //  stepM(stepsPerRevolution*-1);
    //  M1_CW( 255,1000);
      M3_CW(150);
     // M2_CCW(200,150);
      //M1_CW( 150,500);
      M3_CCW(150);
        Flush();
        break;
    
      case '2' :    
      //M2_getback(30, 100, 300);
  //    Serial.println("case 1 : Done");
  //    Serial.println('A');
      Flush();
      break;

      case '3' :
      M2_stop();
  //    Serial.println("case 1 : Done");
  //    Serial.println('3');
      Flush();
      break;
    
      default :
      Serial.println(in_data);
      Serial.println("Err /n");
      break;
    }
  }
 // Serial.print ("Pulse : ");
 // Serial.println(M3_duration);
}

void Flush()
{
  if(Serial.available() > 0)
  {
    //남은 incoming 버퍼 지우기
    while(Serial.available() > 0)
    {
      Serial.read();
    }
  }
}
