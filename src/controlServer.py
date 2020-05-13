import requests
import threading
import os
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5 import uic
#import Serial
#import RPI.GPIO as GPIO

# machine stat
RVM_STATE_OFF = 0
RVM_STATE_ON = 1

# execute Type
EXEC_RAIL = 1

# Error Type


class RVM_Stat: 

    def __init__(self):

        self.machine_stat = RVM_STATE_OFF
        self.exec_stat = 0
        self.recycling_number = {
            "can" : 0,
            "pet" : 0
        }
        self.error_stat = 0


def check_machine_stat(stat):
    while 1:
        if (stat.machine_stat):
            return "start"


# user interface class
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class1 = uic.loadUiType("untitled.ui")[0]
form_class2 = uic.loadUiType("phoneNumber.ui")[0]

# 화면을 띄우는데 사용되는 Class 선언
class mainWindow(QMainWindow,form_class1) :
    can_num = 0
    pet_num = 0
    phone_number = ""
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.pbtn_test_c.clicked.connect(self.test_c)
        self.pbtn_test_p.clicked.connect(self.test_p)
        self.pbtn_next_page.clicked.connect(self.next_page)

    def ready(self) :
        self.phone_number=phone_window.current_PN
        self.can_num=0
        self.pet_num=0
        self.label_intro.setText("쓰레기를 넣어 주세요.\nphone number : "+self.phone_number)

    def test_c(self) :
        self.can_num +=1
        self.label_can_num.setText(str(self.can_num)+'개')

    def test_p(self) :
        self.pet_num +=1
        self.label_pet_num.setText(str(self.pet_num)+'개')

    def next_page(self) :
        phone_window.ready()
        main_window.close()
        phone_window.show()
        

class phoneWindow(QMainWindow, form_class2) :
    current_PN = ""
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.button_0.clicked.connect(lambda: self.buttonClick(0))
        self.button_1.clicked.connect(lambda: self.buttonClick(1))
        self.button_2.clicked.connect(lambda: self.buttonClick(2))
        self.button_3.clicked.connect(lambda: self.buttonClick(3))
        self.button_4.clicked.connect(lambda: self.buttonClick(4))
        self.button_5.clicked.connect(lambda: self.buttonClick(5))
        self.button_6.clicked.connect(lambda: self.buttonClick(6))
        self.button_7.clicked.connect(lambda: self.buttonClick(7))
        self.button_8.clicked.connect(lambda: self.buttonClick(8))
        self.button_9.clicked.connect(lambda: self.buttonClick(9))
        self.button_bs.clicked.connect(self.bsClick)
        self.button_enter.clicked.connect(self.enClick)

    def ready(self) :
        self.current_PN=""
        self.phone_number.setText(str(self.current_PN))

    def buttonClick(self, num) :
        self.current_PN = self.current_PN + str(num)
        self.phone_number.setText(str(self.current_PN))

    def bsClick(self) :
        self.current_PN = self.current_PN[:-1]
        self.phone_number.setText(str(self.current_PN))

    def enClick(self) :
        phone_window.close()
        main_window.ready()
        main_window.show()

if __name__ == '__main__':
    
    RVM_status = RVM_Stat() # stat class init

    #시리얼 통신 인터페이스 init



    # 유저 인터페이스 init
    app = QApplication(sys.argv) 
    phone_window = phoneWindow() 
    main_window = mainWindow()

    phone_window.show()

    t1 = threading.Thread(target = app.exec_())
    t1.daemon = True
    t1.start()


    # main cycle
    while 1:

        #debug
        print("debug msg")
        time.sleep(3)

        #1 machine stat check
        retval = check_machine_stat(RVM_status)
        if (retval < 0):
            print("error")


        #2 initial condition check


        #3 rail move command 


        #4 판별 요청
        resultD = requests.get("URL")


        # 분류기 작동
        #retval = finalCommand(resultD)


        # 스탯 업데이트
        #update_status()



"""
main cycle 
        1. machine stat check

        2. initial condition check

        3. rail move command

        4. 판별 요청 

        5. 분류기 작동

        6. 최종 이동

        7. update status

"""