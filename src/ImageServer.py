from flask import Flask, request
import os
import sys
import subprocess
import time
import random
import argparse

# 디버그 모드 명령행 인자 설정 
parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest = 'debug', action = 'store_true')
args = parser.parse_args()
debug = args.debug

cmd_capture = "rm -rf *.jpg && nvgstcapture-1.0 --cus-prev-res=1920x1080 -A"
cmd_yolo = "./darknet detector test data/obj.data cfg/yolov3.cfg backup/yolov3_last.weights rvm/image/*.jpg >> detect.txt"

app = Flask(__name__)

def parse_result(file_name, threshold):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    lines = lines[1:]
    can = []
    pet = []

    # empty result => 'return'
    if not lines:
        return 'return'

    for i in range(len(lines)):
        lines[i] = lines[i].replace(":", "")
        lines[i] = lines[i].replace("%", "")
        lines[i] = lines[i].replace("\n", "")
        each = lines[i].split()
        if(each[0] == 'pet'):
            pet.append(int(each[1]))
        else:
            can.append(int(each[1]))
    can_possibility = sum(pet)/len(pet)
    pet_possibility = sum(pet)/len(pet)

    if (max(can_possibility, pet_possibility) < threshold or can_possibility==pet_possibility):
        return 'return'
    elif (can_possibility > pet_possibility):
        return 'pet'
    elif (can_possibility < pet_possibility):
        return 'can'

@app.route('/')
def index():
    return 'OK'

@app.route('/requestd', methods = ['POST'])
def start_discrimination():
    
    # debugging code
    if debug:
        q = random.randint(1,10)
        if q <= 2:
            return 'return'
        elif q > 2 and q <= 8:
            return 'pet'
        elif q > 8 and q <= 10:
            return 'can'

    else:

        # Image capture
        try:
            subprocess.call(cmd_capture, shell=True, timeout=4)
        except subprocess.TimeoutExpired:
            print("Timeout during execution")
            return -1

        # Run Yolo
        try:
            subprocess.call(cmd_yolo, shell=True, timeout=10)
        except subprocess.TimeoutExpired: 
            print("Timeout during execution")
            return -1
        
        # Parse result file
        petOrCan= parse_result('./detect.txt', 50)

        return petOrCan

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', threaded=False, debug=False, port=5000)