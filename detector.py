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
from utils.datasets import LoadStreams, LoadImages, letterbox
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, save_one_box, create_folder
from utils.plots import plot_one_box
from utils.torch_utils import select_device, time_synchronized


def detect(src, model):
    source, view_img, imgsz, show_conf, show_fps = src, True, 512, True, False
    # print(source,view_img,imgsz,show_conf,show_fps,opt.device,opt.augment)
    webcam = False  # source.isnumeric() or source.endswith('.txt') or source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    # Directories

    device = select_device('')
    half = device.type != 'cpu'  # half precision only supported on CUDA

    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(512, s=32)  # check img_size
    if half:
        model.half()  # to FP16

    # Set Dataloader
    vid_path, vid_writer = None, None
    '''if webcam:
        view_img = check_imshow()
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz, stride=stride)
    else:'''
    img_size_ds = 512
    stride_ds = 32
    im0s = cv2.cvtColor(np.array(source), cv2.COLOR_RGB2BGR)
    img = letterbox(im0s, img_size_ds, stride=stride_ds)[0]
    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    # dataset = LoadImages(source, img_size=imgsz, stride=stride)

    # Get names and colors
    names = model.module.names if hasattr(model, 'module') else model.names
    colors = (
    (0, 52, 255), (121, 3, 195), (176, 34, 118), (87, 217, 255), (69, 199, 79), (233, 219, 155), (203, 139, 77),
    (214, 246, 255))

    # Run inference
    if device.type != 'cpu':
        model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(model.parameters())))  # run once
    t0 = time.time()

    # for path, img, im0s, vid_cap in dataset:

    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    t1 = time_synchronized()
    pred = model(img, augment=False)[0]

    # Apply NMS
    pred = non_max_suppression(pred, 0.5, 0.45, agnostic=False)
    t2 = time_synchronized()

    # Process detections
    for i, det in enumerate(pred):  # detections per image
        '''if webcam:  # batch_size >= 1
            p, s, im0, frame = path[i], '%g: ' % i, im0s[i].copy(), dataset.count
        else:'''
        s, im0, frame = '', im0s.copy(), 0  # getattr(dataset, 'frame', 0)

        # p = Path(p)  # to Path
        s += '%gx%g ' % img.shape[2:]  # print string
        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

            # Print results
            for c in det[:, -1].unique():
                n = (det[:, -1] == c).sum()  # detections per class
                s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string
            images = []
            for *xyxy, conf, cls in reversed(det):
                x1, y1, x2, y2 = xyxy
                images.append(im0.astype(np.uint8)[int(y1):int(y2), int(x1): int(x2)])

            # print(det)
            if images:
                emotions = detect_emotion(images, show_conf)
                # print(emotions)
                l_cordinates = det.tolist()
                # print(l_cordinates)
                return (l_cordinates, emotions)

            # Write results
            # i = 0
            # for *xyxy, conf, cls in reversed(det):
            #
            #     if view_img or not nosave:
                    # Add bbox to image with emotions on
                    # label = emotions[i][0]
                    # colour = colors[emotions[i][1]]
                    # i += 1
                    ####print(label) ------------------------------------------####
                    # plot_one_box(xyxy, im0, label=label, color=colour, line_thickness=2)

        # Stream results
        '''
        if view_img:
            display_img = cv2.resize(im0, (im0.shape[1]*2,im0.shape[0]*2))
            cv2.imshow("Emotion Detection",display_img)
            cv2.waitKey(1)  # 1 millisecond



    if show_fps:
        # calculate and display fps
        print(f"FPS: {1/(time.time()-t0):.2f}"+" "*5,end="\r")
        t0 = time.time()
    '''

