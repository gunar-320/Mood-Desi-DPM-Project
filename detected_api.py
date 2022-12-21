import detector
import json
import argparse
import time
import os
from pathlib import Path
import numpy as np
from PIL import Image

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from emotion import detect_emotion, init

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, save_one_box, create_folder
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized


class Object(object):
    def __init__(self):
        self.name = "Emotion classification api"

    def toJSON(self):
        return json.dumps(self.__dict__)


# Initialize
set_logging()
device = select_device('')
init(device)
model = attempt_load("weights/yolo.pt", map_location=device)  # load FP32 model




def emo(img):

    emoOutput = detector.detect(img,model)
    #print(len(emoOutput))

    output = []
    item = Object()

    if (emoOutput != None):
        item.numPerson = len(emoOutput[1])
        output.append(item)

        for i in range(0, len(emoOutput[1])):
            #class_name = category_index[classes[c]]['name']
            item = Object()
            item.name = 'person' +str(i)
            #item.class_name = class_name
            item.emotion = emoOutput[1][i]
            item.xt = emoOutput[0][i][0]
            item.yt = emoOutput[0][i][1]
            item.xb = emoOutput[0][i][2]
            item.yb = emoOutput[0][i][3]
            output.append(item)
    else:
        item.numPerson = 0
        output.append(item)

        item0 = Object()
        item0.name = 'No one'
        # item.class_name = class_name
        item0.emotion = ["No person Detected",-1]
        item0.xt = 0
        item0.yt = 0
        item0.xb = 20
        item0.yb = 20

        output.append(item0)

    outputJson = json.dumps([ob.__dict__ for ob in output])

    return outputJson




'''
PATH_TO_TEST_IMAGES_DIR = 'test_images'  # cwh
TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(8)]

image = Image.open(TEST_IMAGE_PATHS[0])

for i in TEST_IMAGE_PATHS:
    print(emo(Image.open(i)))'''
#print(emo(image))
#print(emo(Image.open('group.jpg')))
#print(emo('sam.jpeg'))

