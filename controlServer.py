import requests
import threading
import os
import sys
import time
#import Serial
#import RPI.GPIO as GPIO

from uitest import *

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
app = QApplication(sys.argv) 

phone_window = phoneWindow() 
main_window = mainWindow()

phone_window.show()

if __name__ == '__main__':
    
    RVM_status = RVM_Stat() # stat class init

    #시리얼 통신 인터페이스 init



    # 유저 인터페이스 init
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