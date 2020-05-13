from flask import Flask, request
import os
import sys
import subprocess
import time

app = Flask(__name__)

@app.route('/')
def index():
    return 'OK'

@app.route('/requestd', methods = ['POST'])
def start_discrimination():
    

    # YOLO 실행하는 내용 추가하세요..... 
    
    
    return 'pet'
    



def main():
    app.run(host='0.0.0.0', threaded=True, debug=False, port=5000)


if __name__ == '__main__':
    main()