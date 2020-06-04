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
        pass
        # YOLO 실행하는 내용 추가하세요..... 
        """
        args = './darknet detect yolov3.cfg  backup/without_crawler/yolov3_10000.weights data/test/test_10.jpg -threshold 0.7 >> test_result_wocrawler_v1.txt'
        subprocess.call(args, shell=True)
        """


    

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', threaded=False, debug=False, port=5000)