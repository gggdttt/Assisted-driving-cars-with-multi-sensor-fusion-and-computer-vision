# 树莓派获取来自pc 的数据的方法（主要是控制信号和识别结果）
import socket  # 导入 socket 模块
import struct
import time
from ast import literal_eval
from configparser import ConfigParser
import multiprocessing

import numpy

import MotionModle
import RPi.GPIO as GPIO

import ConnectSerial
import SmartDriving



def config():
    # 初始化配置读取
    config = ConfigParser()
    config.read("xbai_raspberry_setting.ini")
    config.sections()
    return config
    # 读取配置完成


def receive_detected_result(queue_detected_result):
    # 接收socket发来的消息
    computer_server_detected_result_host = config().get('raspberry_server_setting',
                                                        'computer_server_detected_result_host')  # 获取pc的ip地址
    computer_server_detected_result_port = config().getint('raspberry_server_setting',
                                                           'computer_server_detected_result_port')  # 设置端口号
    while True:
        # time.sleep(0.05)
        computer_server_detected_result_socket = socket.socket()  # 创建 socket 对象
        computer_server_detected_result_socket.connect(
            (computer_server_detected_result_host, computer_server_detected_result_port))
        raw_msglen = computer_server_detected_result_socket.recv(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # print(f'{datetime.datetime.now()}:{msglen}')
        data = bytearray()
        while len(data) < msglen:
            packet = computer_server_detected_result_socket.recv(msglen - len(data))
            if not packet:
                return None
            data.extend(packet)

        computer_server_detected_result_socket.close()
        # if queue_convey_detected_result.full():
        #     queue_convey_detected_result.get()
        #     queue_convey_detected_result.put(receive_message)  # 将message 放入queue中，传输给signal_control 端
        # else:
        detected_result = literal_eval(str(data, 'utf-8'))
        while not queue_detected_result.empty():
            queue_detected_result.get()
        for i in detected_result:
            temp = str(i[0], 'utf-8')
            # print(temp)
            if temp == 'person' or temp == 'bottle':
                # print(f'[SmartDriving:smart_driving]:line55:有人')
                queue_detected_result.put(True)
                break
        queue_detected_result.put(False)
        # print('success!')


def receive_control_signal(conn_control_signal_send):
    computer_server_control_signal_host = config().get('raspberry_server_setting',
                                                       'computer_server_control_signal_host')  # 获取pc的ip地址
    computer_server_control_signal_port = config().getint('raspberry_server_setting',
                                                          'computer_server_control_signal_port')  # 设置端口号

    while True:
        try:
            computer_server_control_signal_socket = socket.socket()  # 创建 socket 对象
            computer_server_control_signal_socket.settimeout(20)
            computer_server_control_signal_socket.connect(
                (computer_server_control_signal_host, computer_server_control_signal_port))
            receive_message = computer_server_control_signal_socket.recv(1024)
            control_signal = str(receive_message.decode('utf-8')).strip()
            computer_server_control_signal_socket.close()
            # 1=前进，2=后退，3 = 左，4 =右， 0 = stop
            if control_signal == 'up':
                conn_control_signal_send.send('up')
                # print(f'[RaspberryServer]{control_signal}')
                # car_condition = 1
            elif control_signal == 'down':
                conn_control_signal_send.send('down')
                # car_condition = 2
            elif control_signal == 'right':
                conn_control_signal_send.send('right')
                # car_condition = 3
            elif control_signal == 'left':
                conn_control_signal_send.send('left')
                # car_condition = 4
            elif control_signal == 'stop':
                conn_control_signal_send.send('stop')
        except socket.timeout:
            print('超时啦！')
