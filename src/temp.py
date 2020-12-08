#!/usr/bin/python3
#-*-coding:utf-8 -*-

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
    from hx711 import HX711


####################################################################################
#                                    Data Type                                     #
####################################################################################

# machine stat
RVM_STATE_OFF = 0
RVM_STATE_ON = 1

# execute Type
EXEC_NONE_TYPE = 0
EXEC_LOADCELL_TYPE = 1
EXEC_DCMOTOR_TYPE = 2
EXEC_LINEARMOTOR_TYPE = 3
EXEC_IMAGEPROCESS_TYPE = 4

# Error Type
retValOK = 1
Error = -1

# Rasp GPIO Pin
IR_Pin1 = 6         # Boad(5)
IR_Pin2 = 13         # Boad(7)
IR_Pin3 = 19        # Boad(11)
IR_Pin4 = 26        # Boad(13)

LC_DT_Pin = 23      # Boad(16)
LC_SCK_Pin = 24     # Boad(18)


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
            main_window.end_report()
            while(self.exec_stat):
                continue
            self.recycling_number['can'] = 0
            self.recycling_number['pet'] = 0
        else:
            self.exec_stat = EXEC_NONE_TYPE
            time.sleep(2)



    def putTrashIntoRVM(self, result):
        if result == 'can':
            self.recycling_number['can'] += 1
        elif result == 'pet':
            self.recycling_number['pet'] += 1



# user interface class
# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class1 = uic.loadUiType("ui/new1.ui")[0]
form_class2 = uic.loadUiType("ui/phoneNumber.ui")[0]
form_class3 = uic.loadUiType("ui/newpop2.ui")[0]
form_class4 = uic.loadUiType("ui/newpop1.ui")[0]



def printE(mesg) :
    #main_window.error_pop(mesg)
    main_window.show_popup_ok_cancel('a','b')



class error_sig(QObject) :

    signal1 = pyqtSignal(int)

    def on(self, f):
        self.signal1.emit(f)

class end_sig(QObject) :

    signal1 = pyqtSignal()

    def on(self):
        self.signal1.emit()

class mes_sig(QObject) :

    signal1 = pyqtSignal(str)

    def on(self,m):
        self.signal1.emit(m)


# 화면을 띄우는데 사용되는 Class 선언
class mainWindow(QMainWindow,form_class1) :

    m1 = '쓰레기를 넣어 주세요'
    m2 = ''
    def __init__(self) :
        super().__init__()
        self.fontDB = QFontDatabase()
        self.fontDB.addApplicationFont(":/font/font/12롯데마트드림Bold.ttf")
        self.fontDB.addApplicationFont(":/font/font/12롯데마트행복Bold.ttf")
        self.setupUi(self)
        self.p2_1.setStyleSheet('color:black')
        self.p2_2.setStyleSheet('color:black')
        self.title = '<html><head/><body><p align="center" style = "vertical-align:middle"><span style=" font-size:120pt; ">RVM</span><span style=" font-size:24pt; color:#000000;">(일사분란착착착)</span></p></body></html>'
       
        self.p3.clicked.connect(self.button_start)
        self.p2.setStyleSheet('background-image:url(":/newPrefix/img/pic2.png")')
        self.err_sig = error_sig()
        self.end_sig = end_sig()
        self.mes_sig = mes_sig()
        self.err_sig.signal1.connect(self.error_pop)
        self.end_sig.signal1.connect(self.end_pop)
        self.mes_sig.signal1.connect(self.set_message)


    def set_message_big(self,message) :
        self.m1 = message
        self.mes_sig.on('normal')

    def set_message_small(self,message) :
        self.m2 = message
        self.mes_sig.on('normal')

    def set_message(self,m) :
        if m == 'normal' :
            self.p1.setText('<html><head/><body><p align="center"><span style=" font-size:47pt; color:#000000;">%s</span></p><p align="center"><span style=" font-size:30pt; color:#000000;">%s</span></p></body></html>' %(self.m1,self.m2))
        elif m == 'title' :
            self.p1.setText(self.title)
        elif m == 'ready':
            self.p1.setText('페트병 혹은 캔을\n하나씩 넣어주세요')
    def can_pet(self) :
        self.p2_1.setText(str(RVM_status.recycling_number['pet'])+' 개')
        self.p2_2.setText(str(RVM_status.recycling_number['can'])+' 개')
        

    

    # 시작, 종료 버튼 기능
    def button_start(self) :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            RVM_status.startRVM()
            self.button_text()
        elif RVM_status.machine_stat == RVM_STATE_ON:
            RVM_status.terminationRVM()
            self.button_text()
            
    
    def button_text(self) :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            if RVM_status.exec_stat != EXEC_NONE_TYPE:
                pass
            else :
                self.mes_sig.on('title')
                self.p2.setStyleSheet('background-image:url(":/newPrefix/img/pic2.png")')
                self.p2_2.setText('')
                self.p2_1.setText('')
                self.p3.setText('시작')
        elif RVM_status.machine_stat == RVM_STATE_ON:
            if RVM_status.exec_stat <= EXEC_IRSENCOR_TYPE:
                self.mes_sig.on('ready')
                self.p2.setStyleSheet('background-image:url(":/newPrefix/img/pic4.png")')
                self.can_pet()
                self.p3.setText('종료')
    
    def error_report(self,f):
        self.err_sig.on(f)

    def error_pop(self,mesg) :
        self.set_message_big('에러가 발생했습니다.')
        self.set_message_small('Error')

        p = errPopDialog()
        p.exec_()
        

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
        self.num.setText('에러 발생 \nStep %s' %RVM_status.exec_stat)
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
        self.p = RVM_status.recycling_number['pet']
        self.c = RVM_status.recycling_number['can']
        self.t = self.p + self.c
        self.num.setText('결과 알려드림\n페트병 %d개, 캔 %d개\n총 %d개 들어왔음' %(self.p, self.c, self.t))
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

        #0 machine stat check
        if RVM_status.machine_stat == RVM_STATE_OFF:
            time.sleep(0.1)
            continue

        #2 Check Load cell 
        if checkLoadCell() < 0:
            errorExit()

        result = imageProcess()

        if result == 'invaild':
        
        else:
            

        #3 Linear motor move command 
        elif moveCommand('linear') < 0:
            errorExit()

        #4 Request discrimination
        else :
            resultD = imageProcess()

            #5 rail move command 
            if moveCommand(resultD)<0:
                errorExit()

        if RVM_status.error_stat == retValOK:
            # Update Status
            RVM_status.updateStatus(resultD)

        elif RVM_status.error_stat == Error :
            #debug msg
            while RVM_status.error_stat == Error :
                continue

            printU("Error fixed.. restart")
            main_window.button_text()

                

def errorExit():
    if RVM_status.error_stat == Error:
        return 
    
    RVM_status.error_stat=Error
    main_window.error_report(RVM_status.exec_stat)

#IR sensor
def checkObjectCond():
    RVM_status.exec_stat = EXEC_IRSENCOR_TYPE

    if debug:
        time.sleep(2)
    else:
        # End cycle by pressing the End button before placing the object
        while GPIO.input(IR_Pin1) and \
            GPIO.input(IR_Pin2) and \
            GPIO.input(IR_Pin3) and \
            GPIO.input(IR_Pin4):

            if RVM_status.machine_stat == RVM_STATE_OFF:
                return Error
            time.sleep(0.1)

    printB('쓰레기를 처리중 입니다')
    printU("#1 : 적외선 센서 탐지 중")

    return retValOK

def checkLoadCell():
    RVM_status.exec_stat = EXEC_LOADCELL_TYPE
    printB('쓰레기를 처리중 입니다')
    printU('#2 : 물체 무게 측정 중')

    if debug:
        time.sleep(2)
        return retValOK
    else:
        while 1:
            weights = loadcell.get_raw_data(20)

            weights.remove(max(weights))
            weights.remove(min(weights))

            avg = sum(weights) / len(weights)

            if avg < init_weight-3000 and avg > init_weight-80000:  # 수정 필요
                printB('쓰레기를 처리중 입니다')
                return retValOK
            else:
                printB('쓰레기의 무게가 초과되었습니다.')

            time.sleep(0.5)

def moveCommand(destination):
    count = 0

    if destination == 'linear':
        RVM_status.exec_stat = EXEC_RAIL_TYPE
        printU("#3 : 판별부까지 이동 중")

        if debug:
            time.sleep(1)
            return retValOK
        else:
            ser.write('1'.encode())
            while(ser.readable()):
                ret = ser.read()
                print(ret)
                if ret.decode() == 'y':
                    return retValOK
                elif count > 10:
                    return Error
                else:
                    count += 1
                    

    elif destination == 'pet':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        printU("#5 : 페트병 분류 중")

        if debug:
            time.sleep(1)
            return retValOK
        else:
            ser.write('2'.encode())

            while(ser.readable()):

                ret = ser.read()
                print(ret)
                if ret.decode() == 'y':
                    return retValOK
                elif count > 10:
                    return Error
                else:
                    count += 1

    elif destination == 'can':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        printU("#5 : 캔 분류 중")

        if debug:
            time.sleep(1)
            return retValOK
        else:
            ser.write('3'.encode())
            
            
            while(ser.readable()):
                ret = ser.read()
                print(ret)
                if ret.decode() == 'y':
                    return retValOK
                elif count > 10:
                    return Error
                else:
                    count += 1
    
    else:
        return Error

def requestD():
    RVM_status.exec_stat = EXEC_IMAGEPROCESS_TYPE
    printU("#4 : 물체 판별 중")   
    
    #linux
    try:
        response = requests.post("http://10.0.0.0:5000/requestd")
    except:
        return errorExit()
    
    # window(debug)
    # response = requests.post("http://localhost:5000/requestd")

    return response.text

####################################################################################
#                                   main sequence                                  #
####################################################################################

# stat class init
RVM_status = RVM_Stat() 

if not debug:
    # USB serial interface
    port = '/dev/ttyACM0'                           
    ser = serial.Serial(port, 9600, timeout = 2)


    # Load Cell GPIO setting
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    loadcell = HX711(LC_DT_Pin, LC_SCK_Pin)
    loadcell.reset()

    
    init_weight = sum(loadcell.get_raw_data(30)) / 30

    # IR Sensor GPIO setting
    GPIO.setup(IR_Pin1,GPIO.IN)
    GPIO.setup(IR_Pin2,GPIO.IN)
    GPIO.setup(IR_Pin3,GPIO.IN)
    GPIO.setup(IR_Pin4,GPIO.IN)

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

