import os
import subprocess
import time

cmd_yolo = "./darknet detector test data/obj.data cfg/yolov3.cfg backup/yolov3_last.weights rvm/image/test_1.jpg"

def test_yolo():
    try:
        subprocess.call(cmd_yolo, shell=True, timeout=10)
    except subprocess.TimeoutExpired: 
        print("Timeout during execution")   


def main():
    test_yolo2()

if __name__ == '__main__':
    main()
