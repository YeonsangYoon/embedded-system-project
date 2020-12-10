import time
import cv2
import torch
from torchvision import transforms
from torchvision import models
import torch.nn as nn
from PIL import Image
import os

def image_precess():
    start = time.time()
    os.system('sudo fswebcam -d /dev/video1 --no-banner /home/jetsontx1/young/finalProject/youngs_test_before.jpg')
    img = cv2.imread("/home/jetsontx1/young/finalProject/youngs_test_before.jpg", cv2.IMREAD_COLOR)
    crop_pre = img[80:250,90:300]
    cv2.imwrite('/home/jetsontx1/young/finalProject/youngs_test_after.jpg', crop_pre)

    preprocess = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )])

    # model_ft = models.resnet34()
    # num_ftrs = model_ft.fc.in_features
    # model_ft.fc = nn.Linear(num_ftrs, 2)
    # model_ft.load_state_dict(torch.load("./model/output_two_can_pet_data_v5_34layer.pth"))
    # model_ft.eval().cuda()

    image = Image.open('youngs_test_after.jpg')

    img = preprocess(image).cuda()
    batch_t = torch.unsqueeze(img, 0)
    result = model_ft(batch_t)
    percentage = torch.nn.functional.softmax(result, dim=1)[0] * 100
    if(percentage == max(percentage)).nonzero().item() == 1:
        waste = "pet"
    else:
        waste = "can"

    print(waste + " ", max(percentage).item())
    print("time :", time.time() - start)
    return waste

if __name__=="__main__":
    model_ft = models.resnet34()
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, 2)
    model_ft.load_state_dict(torch.load("./model/output_two_can_pet_data_v5_34layer.pth"))
    model_ft.eval().cuda()
    image_precess()