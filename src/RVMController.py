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
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import argparse
import serial

# 디버그 모드 명령행 인자 설정 
parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest = 'debug', action = 'store_true')
args = parser.parse_args()
debug = args.debug

if debug == False:
    import RPi.GPIO as GPIO


####################################################################################
#                                    Data Type                                     #
####################################################################################

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


####################################################################################
#                                Class & Functions                                 #
####################################################################################

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
        if result == 'pet':
            printB('페트병 하나 처리되었습니다')
            printU("1 trash complete")
            self.recycling_number['pet'] += 1
        elif result == 'can':
            printB('캔 하나 처리되었습니다')
            printU("1 trash complete")
            self.recycling_number['can'] += 1
        elif result == 'return':
            printB('잘못된 쓰레기를 다시 반송합니다')
            printU('1 trash return')

        if self.machine_stat == RVM_STATE_OFF:
            time.sleep(2)
            main_window.end_report()
            while(self.exec_stat):
                continue
            self.recycling_number['can'] = 0
            self.recycling_number['pet'] = 0
        else:
            self.exec_stat = EXEC_NONE_TYPE



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
form_class3 = uic.loadUiType("popup.ui")[0]
form_class4 = uic.loadUiType("popup2.ui")[0]



def printE(mesg) :
    #main_window.error_pop(mesg)
    main_window.show_popup_ok_cancel('a','b')
    '''ep = errorPOP
    ep.show()
    print('a')
    app2 = QApplication(sys.argv) 
    app2.exec_()
    print('a')'''


class error_sig(QObject) :

    signal1 = pyqtSignal(int)

    def on(self, f):
        self.signal1.emit(f)

class end_sig(QObject) :

    signal1 = pyqtSignal()

    def on(self):
        self.signal1.emit()

# 화면을 띄우는데 사용되는 Class 선언
class mainWindow(QMainWindow,form_class1) :

    m1 = '쓰레기를 넣어 주세요'
    m2 = ''
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        #self.pbtn_test_c.clicked.connect(self.test_c)
        #self.pbtn_test_p.clicked.connect(self.test_p)
        self.pbtn_start.clicked.connect(self.button_start)
        self.err_sig = error_sig()
        self.end_sig = end_sig()
        self.err_sig.signal1.connect(self.error_pop)
        self.end_sig.signal1.connect(self.end_pop)

        self.qPixmapVar = QPixmap()
        self.qPixmapVar.load('img/can.PNG')
        self.label_10.setPixmap(self.qPixmapVar)
        self.qPixmapVar.load('img/pet.PNG')
        self.label_17.setPixmap(self.qPixmapVar)


    def set_message_big(self,message) :
        self.m1 = message
        self.label_intro.setText(self.m1)

    def set_message_small(self,message) :
        self.m2 = message
        self.label_intro_2.setText(self.m2)

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
    
    def error_report(self,f):
        self.err_sig.on(f)

    def error_pop(self,mesg) :
        self.set_message_big('에러가 발생했습니다.')
        self.set_message_small('Error')

        p = errPopDialog()
        p.exec_()
        
        """
        qmb =QMessageBox()
        result = qmb.warning(self,'Error','error occurs in step %s' %mesg,QMessageBox.Ok)
        if result == QMessageBox.Ok :
            RVM_status.error_stat=retValOK
        """

    def end_report(self):
        self.end_sig.on()
    
    def end_pop(self):
        p = endPopDialog()
        p.exec_()


def printU(mesg) :
    main_window.set_message_small(mesg)

def printB(mesg) :
    main_window.set_message_big(mesg)

class errPopDialog(QDialog,form_class3):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label_err_mesg.setText('Error occurs in\nStep %s' %RVM_status.exec_stat)
        self.pushButton.clicked.connect(self.errorOk)

    def errorOk(self):
        RVM_status.terminationRVM()
        RVM_status.updateStatus(0)
        self.close()
        RVM_status.error_stat = retValOK
        

class endPopDialog(QDialog,form_class4):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.can_num.setText('can : %s개' %RVM_status.recycling_number['can'])
        self.pet_num.setText('pet : %s개' %RVM_status.recycling_number['pet'])
        self.pushButton.clicked.connect(self.endOk)

    def endOk(self):
        RVM_status.exec_stat = EXEC_NONE_TYPE
        self.close()
    
            
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

        if RVM_status.machine_stat != RVM_STATE_ON:     #1 machine stat check
            printB('start 버튼을 눌러주세요')
            printU('')
            time.sleep(0.5)
        else :
            #2 initial condition check
            if checkObjectCond() < 0:
                errorExit()

            elif checkLoadCell() < 0:
                errorExit()

            #3 rail move command 
            elif moveCommand('Dzone') < 0:
                errorExit()

            #4 판별 요청
            else :
                resultD = requestD()
                if moveCommand(resultD)<0:
                    errorExit()

            if RVM_status.error_stat == retValOK:
                # 스탯 업데이트
                RVM_status.updateStatus(resultD)
                main_window.can_pet()
                time.sleep(3)
                main_window.button_text()

            elif RVM_status.error_stat == Error :
                #debug msg
                while RVM_status.error_stat == Error :
                    continue
                
                printU("Error fixed.. restart")
                time.sleep(2)
                main_window.button_text()

                

def errorExit():
    if RVM_status.error_stat == Error:
        return 
    
    RVM_status.error_stat=Error
    main_window.error_report(RVM_status.exec_stat)

#IR sensor
def checkObjectCond():
    RVM_status.exec_stat = EXEC_IRSENCOR_TYPE
    printB('쓰레기를 넣어 주세요')
    printU("#2 : check object condition")

    if debug:
        time.sleep(2)
    else:
        while GPIO.input(11):
            pass

    return retValOK

def checkLoadCell():
    RVM_status.exec_stat = EXEC_LOADCELL_TYPE
    printB('쓰레기 처리중 입니다')
    printU('#3 : check object weight')
    
    if debug:
        time.sleep(3)

    return retValOK

def moveCommand(destination):
    if destination == 'can':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        printU("#6 : moving to can zone")

        if debug:
            time.sleep(3)

        return retValOK

    elif destination == 'pet':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        printU("#6 : moving to pet zone")

        if debug:
            time.sleep(2)
        else:
            serialToArduino.writelines('1')

        return retValOK

    elif destination == 'Dzone':
        RVM_status.exec_stat = EXEC_RAIL_TYPE
        printU("#4 : moving to discriminating zone")

        if debug:
            time.sleep(3)

        return retValOK

    elif destination == 'return':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        printU("#6 : moving to entrance")

        if debug:
            time.sleep(3)
            
        return retValOK

    else:
        return Error

def requestD():
    RVM_status.exec_stat = EXEC_IMAGEPROCESS_TYPE
    printU("#5 : discriminating image")

    #linux
    try:
        response = requests.post("http://0.0.0.0:5000/requestd")
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

if not debug:
    # USB serial interface
    port = '/dev/ttyACM0'                           
    serialToArduino = serial.Serial(port, 9600)

    # GPIO setting
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.IN)

# 유저 인터페이스 init
app = QApplication(sys.argv) 
phone_window = phoneWindow() 
main_window = mainWindow()
main_window.showFullScreen()

# main Cycle init
t1 = threading.Thread(target = main_Cycle)
t1.daemon = False

t1.start()

app.exec_()

