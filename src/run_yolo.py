import os
import subprocess
import time

cmd_capture = "rm -rf *.jpg && nvgstcapture-1.0 --cus-prev-res=1920x1080 -A"
cmd_yolo = "./darknet detector test data/obj.data cfg/yolov3.cfg backup/yolov3_last.weights rvm/image/*.jpg >> detect.txt"

def capture_vid():
    try:
        subprocess.call(cmd_capture, shell=True, timeout=4)
    except subprocess.TimeoutExpired:
        print("Timeout during execution")

def test_yolo():
    try:
        subprocess.call(cmd_yolo, shell=True, timeout=10)
    except subprocess.TimeoutExpired: 
        print("Timeout during execution")

def parse_result(file_name, threshold):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    lines = lines[1:]
    can = []
    pet = []
    for i in range(len(lines)):
        lines[i] = lines[i].replace(":", "")
        lines[i] = lines[i].replace("%\n", "")
        each = lines[i].split()
        if(each[0] == 'pet'):
            pet.append(int(each[1]))
        else:
            can.append(int(each[1]))
    can_possibility = sum(pet)/len(pet)
    pet_possibility = sum(pet)/len(pet)

    if (max(can_possibility, pet_possibility) < threshold):
        return 'return'
    elif(can_possibility>pet_possibility):
        return 'pet'
    else:
        return 'can'

def main():
    capture_vid()
    test_yolo()
    petOrCan = parse_result('./detect.txt', 50)

if __name__ == '__main__':
    main()