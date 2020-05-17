"""
This is RVM controller

Components:

    1. User Interface
    2. Main Cycle
    3. RVM status

main cycle:

    1. machine stat check
    2. initial condition check
    3. rail move command
    4. 판별 요청 
    5. 분류기 작동
    6. 최종 이동
    7. update status

"""

import requests, json
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
EXEC_NONE_TYPE = 0
EXEC_IRSENCOR_TYPE = 1
EXEC_LOADCELL_TYPE = 2
EXEC_RAIL_TYPE = 3
EXEC_IMAGEPROCESS_TYPE = 4
EXEC_ROUTING_TYPE = 5

# Error Type
retValOK = 1
Error = -1

class RVM_Stat: 

    def __init__(self):

        self.machine_stat = RVM_STATE_OFF
        self.exec_stat = EXEC_NONE_TYPE
        self.recycling_number = {
            "can" : 0,
            "pet" : 0
        }
        self.error_stat = retValOK

    def startRVM(self):
        self.machine_stat = RVM_STATE_ON
    
    def terminationRVM(self):
        self.machine_stat = RVM_STATE_OFF

    def updateStatus(self, result):
        if self.machine_stat == RVM_STATE_OFF:
            self.exec_stat = EXEC_NONE_TYPE
            self.recycling_number['can'] = 0
            self.recycling_number['pet'] = 0
        else:
            self.exec_stat = EXEC_NONE_TYPE
            if result == 'pet':
                self.recycling_number['pet'] += 1
            elif result == 'can':
                self.recycling_number['can'] += 1

    def putTrashIntoRVM(self, result):
        if result == 'can':
            self.recycling_number['can'] += 1
        elif result == 'pet':
            self.recycling_number['pet'] += 1



# user interface class
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class1 = uic.loadUiType("untitled.ui")[0]
form_class2 = uic.loadUiType("phoneNumber.ui")[0]

def printU(mesg) :
    main_window.show_message(mesg)

# 화면을 띄우는데 사용되는 Class 선언
class mainWindow(QMainWindow,form_class1) :

    #phone_number = ""
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #self.pbtn_test_c.clicked.connect(self.test_c)
        #self.pbtn_test_p.clicked.connect(self.test_p)
        self.pbtn_start.clicked.connect(self.button_start)

    def show_message(self,message) :
        #self.phone_number=phone_window.current_PN
        #self.can_num=0
        #self.pet_num=0
        self.label_intro.setText("쓰레기를 넣어 주세요.\n"+message)

    def can_pet(self) :
        self.label_can_num.setText(str(RVM_status.recycling_number['can'])+'개')
        self.label_pet_num.setText(str(RVM_status.recycling_number['pet'])+'개')

    # 시작, 종료 버튼 기능
    def button_start(self) :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            RVM_status.startRVM()
            self.button_text()
        elif RVM_status.machine_stat == RVM_STATE_ON:
            RVM_status.terminationRVM()
            self.button_text()
            
        #phone_window.ready()
        #main_window.close()
        #phone_window.show()
    
    def button_text(self) :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            if RVM_status.exec_stat != EXEC_NONE_TYPE:
                self.pbtn_start.setText('waiting')
            else :
                self.pbtn_start.setText('start')
        elif RVM_status.machine_stat == RVM_STATE_ON:
            self.pbtn_start.setText('end')

            
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
        main_window.show()


def main_Cycle():
    # main cycle
    while 1:

        print("#1 : check condition....")    #debug
        printU("#1 : check condition....")
        time.sleep(1)
        if RVM_status.machine_stat == RVM_STATE_ON:        #1 machine stat check

            #2 initial condition check
            retval = checkObjectCond()
            if retval < 0:
                errorExit()

            retval = checkLoadCell()
            if retval < 0:
                errorExit()

            #3 rail move command 
            retval = moveCommand('Dzone')
            if retval < 0:
                errorExit()

            #4 판별 요청
            #resultD = requests.get("URL")
            resultD = requestD()

            # 분류기 작동
            retval = moveCommand(resultD)
            if retval < 0:
                errorExit()

            # 스탯 업데이트
            RVM_status.updateStatus(resultD)
            main_window.can_pet()
            main_window.button_text()

            #debug msg
            print("debug msg : 1 trash complete")
            printU("debug msg : 1 trash complete")


def errorExit():
    printU("ERROR %s " %RVM_status.exec_stat)

#IR sensor
def checkObjectCond():
    #debug code
    #print("#2 : check object condition.....")
    RVM_status.exec_stat = EXEC_IRSENCOR_TYPE
    printU("#2 : check object condition.....")
    time.sleep(2)
    return retValOK

def checkLoadCell():

    RVM_status.exec_stat = EXEC_LOADCELL_TYPE
    printU('#3 : check object weight....')
    time.sleep(3)
    return retValOK

def moveCommand(destination):
    if destination == 'can':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        #print("#6 : moving to can zone.....")
        printU("#6 : moving to can zone.....")
        time.sleep(3)
        return retValOK

    elif destination == 'pet':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        #print("#6 : moving to pet zone.....")
        printU("#6 : moving to pet zone.....")
        time.sleep(3)
        return retValOK

    elif destination == 'Dzone':
        RVM_status.exec_stat = EXEC_RAIL_TYPE
        #print("#4 : moving to discriminating zone.....")
        printU("#4 : moving to discriminating zone.....")
        time.sleep(3)
        return retValOK

    elif destination == 'return':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        #print("#6 : moving to entrance.....")
        printU("#6 : moving to entrance.....")
        time.sleep(3)
        return retValOK

    else:
        return Error

def requestD():
    RVM_status.exec_stat = EXEC_IMAGEPROCESS_TYPE
    #print("#5 : discriminating image....")
    printU("#5 : discriminating image....")

    #linux
    try:
        response = requests.post("http://0.0.0.0:5000/requestd")
    #except ConnectionRefusedError:
    except:
        return errorExit()
    
    #window(debug)
    #response = requests.post("http://localhost:5000/requestd")

    return response.text

####################################################################################
#                                   main sequence                                  #
####################################################################################

# stat class init
RVM_status = RVM_Stat() 

 
#시리얼 통신 인터페이스 init


# 유저 인터페이스 init
app = QApplication(sys.argv) 

phone_window = phoneWindow() 
main_window = mainWindow()
phone_window.show()

t1 = threading.Thread(target = main_Cycle)
t1.daemon = False

t1.start()

app.exec_()

