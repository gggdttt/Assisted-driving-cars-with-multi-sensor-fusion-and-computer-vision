import struct
from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet
from configparser import ConfigParser
import socket  # 导入 socket 模块


def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax


def cvDrawBoxes(detections, img):
    for detection in detections:
        x, y, w, h = detection[2][0], \
                     detection[2][1], \
                     detection[2][2], \
                     detection[2][3]
        xmin, ymin, xmax, ymax = convertBack(
            float(x), float(y), float(w), float(h))
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        if detection[0] == b'person':
            cv2.rectangle(img, pt1, pt2, (255, 0, 0), 3)
            cv2.putText(img,
                        detection[0].decode() +
                        " [" + str(round(detection[1] * 100, 2)) + "]",
                        (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        [255, 0, 0], 2)
        else:
            cv2.rectangle(img, pt1, pt2, (0, 255, 0), 1)
            cv2.putText(img,
                        detection[0].decode() +
                        " [" + str(round(detection[1] * 100, 2)) + "]",
                        (pt1[0], pt1[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        [0, 255, 0], 2)
    return img


netMain = None
metaMain = None
altNames = None


def readConfigFile():
    # 读取配置文件
    # 我的配置文件是直接放在统一目录下的  xbai_darknet_setting.ini
    config = ConfigParser()
    config.read("xbai_darknet_setting.ini")
    config.sections()
    return config


def loadNetWork():
    config = readConfigFile()
    global metaMain, netMain, altNames
    # 初始化网络
    configPath = config.get('darknet_video_setting', 'configPath')
    weightPath = config.get('darknet_video_setting', 'weightPath')
    metaPath = config.get('darknet_video_setting', 'metaPath')
    if not os.path.exists(configPath):
        raise ValueError("Invalid config path `" +
                         os.path.abspath(configPath) + "`")
    if not os.path.exists(weightPath):
        raise ValueError("Invalid weight path `" +
                         os.path.abspath(weightPath) + "`")
    if not os.path.exists(metaPath):
        raise ValueError("Invalid data file path `" +
                         os.path.abspath(metaPath) + "`")
    if netMain is None:
        netMain = darknet.load_net_custom(configPath.encode(
            "ascii"), weightPath.encode("ascii"), 0, 1)  # batch size = 1
    if metaMain is None:
        metaMain = darknet.load_meta(metaPath.encode("ascii"))
    if altNames is None:
        try:
            with open(metaPath) as metaFH:
                metaContents = metaFH.read()
                import re
                match = re.search("names *= *(.*)$", metaContents,
                                  re.IGNORECASE | re.MULTILINE)
                if match:
                    result = match.group(1)
                else:
                    result = None
                try:
                    if os.path.exists(result):
                        with open(result) as namesFH:
                            namesList = namesFH.read().strip().split("\n")
                            altNames = [x.strip() for x in namesList]
                except TypeError:
                    pass
        except Exception:
            pass


def YOLO(ifShowImg):
    loadNetWork()

    config = readConfigFile()
    # cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(config.get('darknet_video_setting', "raspberry_video_address"))
    cap.set(3, config.getint('darknet_video_setting', "raspberry_video_width"))
    cap.set(4, config.getint('darknet_video_setting', "raspberry_video_height"))
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(darknet.network_width(netMain),
                                       darknet.network_height(netMain), 3)
    # 创建socket和web的传输
    detected_result_to_raspberry_socket = socket.socket()  # 创建 socket 对象
    detected_result_to_raspberry_host = readConfigFile().get('darknet_video_setting',
                                                             "detected_result_to_raspberry_host")  # 获取本地主机名
    detected_result_to_raspberry_port = readConfigFile().getint('darknet_video_setting',
                                                                "detected_result_to_raspberry_port")  # 设置端口
    detected_result_to_raspberry_socket.bind(
        (detected_result_to_raspberry_host, detected_result_to_raspberry_port))  # 绑定端口
    detected_result_to_raspberry_socket.listen(5)  # 等待客户端连接

    while True:
        # 这个循环的作用：循环读取摄像头信息，然后对其进行实时识别之后通过socket传给树莓派和浏览器控制端
        # prev_time = time.time()
        # time.sleep(0.05)
        ret, frame_read = cap.read()
        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb,
                                   (darknet.network_width(netMain),
                                    darknet.network_height(netMain)),
                                   interpolation=cv2.INTER_LINEAR)
        darknet.copy_image_from_bytes(darknet_image, frame_resized.tobytes())
        detections = darknet.detect_image(netMain, metaMain, darknet_image, thresh=0.25)
        # now = int(round(time.time() * 1000))
        # send_message = f'[{now}]:{detections}'
        # print(send_message)

        if ifShowImg:
            image = cvDrawBoxes(detections, frame_resized)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # cv2.namedWindow('detected_result', cv2.WINDOW_NORMAL)
            # cv2.setWindowProperty('detected_result', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.imshow('detected_result', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        connection_to_raspberry, addr = detected_result_to_raspberry_socket.accept()  # 建立和树莓派的socket通信
        send_mess = bytes(str(detections), 'utf-8')
        msg = struct.pack('>I', len(send_mess)) + send_mess
        connection_to_raspberry.sendall(msg)
        # connection_to_raspberry.send(bytes(str(detections), 'utf-8'))
        connection_to_raspberry.close()  # 关闭连接
    cap.release()
    # out.release()


if __name__ == "__main__":
    YOLO(False)
