#!/usr/bin/python3

import RPi.GPIO as GPIO
from hx711 import HX711

LC_DT_Pin = 8
LC_SCK_Pin = 11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

loadcell = HX711(LC_SCK_Pin, LC_DT_Pin)
loadcell.reset()
print(loadcell._read())             # 1개 데이터 읽기
print(loadcell.get_raw_data(10))    # 10개 list로 읽기
GPIO.cleanup()
