import os
import subprocess
import time

cmd_capture = "nvgstcapture-1.0 --cus-prev-res=1920x1080 -A blahblahblah yeon goo sil ga seo sseun dang"
cmd_yolo = "./darknet detector test data/obj.data cfg/yolov3.cfg backup/yolov3_last.weights rvm/image/test_1.jpg >> detect.txt"

def capture_vid():
    try:
        subprocess.call(cmd_yolo, shell=True, timeout=4)
    except subprocess.TimeoutExpired:
        print("Timeout during execution")

def test_yolo():
    try:
        subprocess.call(cmd_yolo, shell=True, timeout=10)
    except subprocess.TimeoutExpired: 
        print("Timeout during execution")

def parse_result(file_name, threshold):
    f = open(file_name)
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
    #0 is idle, 1 is pet, 2 is can
    if (max(can_possibility, pet_possibility) < threshold):
        return 0, 0
    elif(can_possibility>pet_possibility):
        return 1, pet_possibility
    else:
        return 2, can_possibility

def main():
    capture_vid()
    test_yolo()
    petOrCan, possibility = parse_result('D:\workspace_py\darknet_parse\parse_1.txt', 50)

if __name__ == '__main__':
    main()