from flask import Flask, request
import os
import sys
import subprocess
import time
import random
import argparse

from run_yolo import *

# 디버그 모드 명령행 인자 설정 
parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest = 'debug', action = 'store_true')
args = parser.parse_args()
debug = args.debug

app = Flask(__name__)

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
        capture_vid()
        test_yolo()
        petOrCan= parse_result('./detect.txt', 50)

        return petOrCan

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', threaded=False, debug=False, port=5000)