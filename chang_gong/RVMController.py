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

새로운 메인 사이클 

1. 온 오프 확인
2. 로드셀 확인
3. 이미지 판별

4 - 1. 판별 결과 정확
5 - 1. 리니어 모터 동작
6 - 1. DC 모터 동작
7 - 1. 상태 업데이트

4 - 2. 판별 결과 오류
5 - 2. UI에 그대로 투입할지 반환할지 선택

6 - 2 - 1. 그대로 투입하도록 선택함
7 - 2 - 1. 리니어 모터 동작
8 - 2 - 1. DC 모터 동작
9 - 2 - 1. 상태 업데이트

6 - 2 - 2. 반환 선택함
7 - 2 - 2. 사용자에게 반환하도록 일정시간 준다. 
8 - 2 - 2. 상태 업데이트


"""

import requests, json
import threading
import os
import sys
import time
import argparse 
#import serial
import random

from server import *

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
EXEC_IRSENCOR_TYPE = 1
EXEC_LOADCELL_TYPE = 2
EXEC_RAIL_TYPE = 3
EXEC_IMAGEPROCESS_TYPE = 4
EXEC_ROUTING_TYPE = 5

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
        self.user_select = ''   #이게 캔 페트 사용자 입력받는거
        self.force_continue = ''
        self.recycling_number = {
            "can" : 0,
            "pet" : 0
        }
        self.error_stat = retValOK
        self.reset_selection = 0

    def startRVM(self):
        self.machine_stat = RVM_STATE_ON
    
    def terminationRVM(self):
        self.machine_stat = RVM_STATE_OFF

    def updateStatus(self, result):
        if result == 'pet':
            sendMesg('페트병 하나 처리되었습니다')
            self.recycling_number['pet'] += 1
        elif result == 'can':
            sendMesg('캔 하나 처리되었습니다')
            self.recycling_number['can'] += 1
        elif result == 'return':
            sendMesg('잘못된 쓰레기를 다시 반송합니다')

        if self.reset_selection == 1 :
            self.reset_selection = 0
            self.user_select = ''

        if self.machine_stat == RVM_STATE_OFF:
            endReport()
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



def button_text() :
        if RVM_status.machine_stat == RVM_STATE_OFF:
            if RVM_status.exec_stat != EXEC_NONE_TYPE:
                pass
            else :
                #self.mes_sig.on('title')
                #self.p2.setStyleSheet('background-image:url(":/newPrefix/img/pic2.png")')
                #self.p2_1.setText('')
                #self.p2_2.setText('')
                #self.p3.setText('시작')
                setButton('start')
        elif RVM_status.machine_stat == RVM_STATE_ON:
            if RVM_status.exec_stat == EXEC_NONE_TYPE:
                #self.p1.setText('페트병 혹은 캔을\n하나씩 넣어주세요')
                #self.p2.setStyleSheet('background-image:url(":/newPrefix/img/pic4.png")')
                #self.can_pet()
                #self.p3.setText('종료')
                setButton('end')


def main_Cycle():
    # main cycle
    while 1:
        #1. 온 오프 확인
        if RVM_status.machine_stat != RVM_STATE_ON:
            time.sleep(0.1)
        else :
            #1-1. 사용자 캔 페트 입력
            if checkUserInput() < 0:
                RVM_status.updateStatus('')

            else:
                #2. 로드셀 확인
                if checkLoadCell() < 0:
                    pass

                #3. 이미지 판별
                elif dummyImgCheck() < 0:
                    # 4 - 2. 판별 결과 오류
                    if checkForceContinue() < 0:
                        errorExit()
                    
                    elif RVM_status.force_continue == 'yes' :
                        sendMesg('진행')
                        RVM_status.force_continue = ''
                        time.sleep(2)
                        #6 - 2 - 1. 그대로 투입하도록 선택함
                        #7 - 2 - 1. 리니어 모터 동작
                        #8 - 2 - 1. DC 모터 동작
                        #9 - 2 - 1. 상태 업데이트
                        pass

                    elif RVM_status.force_continue == 'no' :
                        sendMesg('반환')
                        RVM_status.force_continue = ''
                        time.sleep(2)
                        #RVM_status.user_select = ''
                        #6 - 2 - 2. 반환 선택함
                        #7 - 2 - 2. 사용자에게 반환하도록 일정시간 준다. 
                        #8 - 2 - 2. 상태 업데이트
                        RVM_status.updateStatus('')
                        continue


                #4-1. 판별 결과 정확
                #5-1. 리니어 모터 동작
                elif dummyLinearCheck() < 0:
                    errorExit()
                
                #6-1. DC 모터 동작
                elif dummyDCCheck() < 0:
                    errorExit()
                    
            #7-1. 상태 업데이트

            if RVM_status.error_stat == retValOK:
                # Update Status
                RVM_status.updateStatus(RVM_status.user_select)
                sendCount()
                button_text()
                time.sleep(2)

            elif RVM_status.error_stat == Error :
                #debug msg
                while RVM_status.error_stat == Error :
                    continue

                sendMesg("Error fixed.. restart")
                button_text()
                time.sleep(2)

                

def errorExit():
    if RVM_status.error_stat == Error:
        return 
    
    RVM_status.error_stat=Error
    error_report(RVM_status.exec_stat)

def checkUserInput():
    if RVM_status.user_select == '' :
        sendMesg('캔 패트 고르기')
        trigger('showButton')
        
        while RVM_status.user_select == '' and RVM_status.machine_stat == 1 :
            pass
    
        if RVM_status.machine_stat == 0 :
            return -1
        
        else :
            sendMesg(RVM_status.user_select + '를 선택함')
            time.sleep(1)
            return 1

    else :
        sendMesg(RVM_status.user_select + '을 넣어주세요')
        return 1

def dummyImgCheck():
    sendCamera('/static/img/sample.jpg')
    time.sleep(5)
    trigger('endCamera')
    return random.randrange(-1,1)

def checkForceContinue():
    sendMesg('계속 진행?')
    trigger('forceContinue')
    while RVM_status.force_continue == '' and RVM_status.machine_stat == 1 :
        pass
    
    if RVM_status.machine_stat == 0 :
        return -1

    else :
        return 1

def dummyLinearCheck():
    sendMesg('리니어모터')
    time.sleep(2)
    return 1

def dummyDCCheck():
    sendMesg('DC모터')
    time.sleep(2)
    return 1

def dummyElseCheck():
    return 1


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

    #printB('쓰레기를 처리중 입니다')
    #printU("#1 : check object condition")
    sendMesg('쓰레기를 처리중 입니다')
    

    return retValOK

def checkLoadCell():
    RVM_status.exec_stat = EXEC_LOADCELL_TYPE
    #printB('쓰레기를 처리중 입니다')
    #printU('#2 : check object weight')

    #sendMesg('로드셀')

    if debug:
        time.sleep(2)
        if RVM_status.user_select == '' :
            return -1
        return retValOK
    else:
        while 1:

            #if RVM_status.user_select == '' :
            #    return -1

            weights = []

            for i in range(20):
                weights.append(hx711._read())

                if False in weights:
                    weights.remove(False)

            weights.remove(max(weights))
            weights.remove(min(weights))

            avg = sum(weights) / len(weights)

            if avg < init_avg-3000 and avg > init_avg-80000:
                #printB('쓰레기를 처리중 입니다')
                return retValOK
            else:
                pass
                #printB('쓰레기의 무게가 초과되었습니다.')
                #sendMesg('무게초과')

            time.sleep(0.5)

def moveCommand(destination):
    count = 0

    if destination == 'Dzone':
        RVM_status.exec_stat = EXEC_RAIL_TYPE
        #printU("#3 : moving to discriminating zone")
        sendMesg('moving to discriminating zone')
        
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
        #printU("#5 : moving to pet zone")
        sendMesg('#5 : moving to pet zone')

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
        #printU("#5 : moving to can zone")
        sendMesg('#5 : moving to can zone')
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
    elif destination == 'return':
        RVM_status.exec_stat = EXEC_ROUTING_TYPE
        #printU("#5 : moving to entrance")


        if debug:
            time.sleep(1)
            return retValOK
        else:
            ser.write('4'.encode())
            
            
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
    #printU("#4 : discriminating image")   
    sendMesg("#4 : discriminating image")
    

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
    hx711 = HX711(LC_DT_Pin, LC_SCK_Pin)
    hx711.reset()

    w = []
        
    for i in range(20):
        w.append(hx711._read())

        if False in w:
            w.remove(False)
        
    w.remove(max(w))
    w.remove(min(w))
    init_avg = sum(w) / len(w)


    # IR Sensor GPIO setting
    GPIO.setup(IR_Pin1,GPIO.IN)
    GPIO.setup(IR_Pin2,GPIO.IN)
    GPIO.setup(IR_Pin3,GPIO.IN)
    GPIO.setup(IR_Pin4,GPIO.IN)

# 유저 인터페이스 init
#app = QApplication(sys.argv) 
#phone_window = phoneWindow() 
#ain_window = mainWindow()
#main_window.showFullScreen()

# main Cycle init
t = threading.Thread(target=socketStart)
t.start()

getClass(RVM_status)

main_Cycle()
