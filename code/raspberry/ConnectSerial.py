# 简介： Delta-2A激光雷达是通过UART TTL电平与外部设备通信的，仅支持单工
# 通讯(即激光雷达主动发数据帧到外部设备)，外部设备只需从数据帧中提取有效
# 数据即可，不需要做任何回应,通讯帧中的所有数据都是16进制格式数据。
# 雷达是旋转测量一周，扫描得到周围一圈均匀分布点的信息（点的角度和距
# 离）。sdk 就是接收解析数据，得到每一圈点的信息。一圈360°被平均分为 16
# 帧上报扫描信息（见下面命令字列表）帧，所以得到 16帧的每帧起始角度分别
# 是0°（零点——位置见规格书）、22.5°、45°、67.5°、90°…270°、292.5°、315、
# 337.5°、360°。16帧数据加起来是完整一圈，一圈的总点数=16*每帧的点数；
# 每帧的总点数根据扫描信息帧计算距离个数可以得到(距离个数=总点数)。每帧
# 数据点的信息(角度和距离)：一帧中第N个点的距离是扫描信息帧中N距离值，
# 那一帧中第N个点距离对应的角度=此帧起始角度+（N-1）*22.5/（每帧的总
# 点数），这样一帧点信息(角度和距离)都有了。
# 依照本文定义的通讯协议解析通讯数据，健康状态信息。
import datetime
import json
import multiprocessing
import socket
import struct
from multiprocessing import Queue
import math
import numpy as np
import serial
import time

# 读取雷达数据相关函数：
import RaspberryServer


def check_code(ser):
    while True:
        check_code = 0x00
        data = ser.read(1).hex()
        # 寻找帧头
        if data == 'aa':
            check_code += 0xaa
            read_data = ser.read(2)
            all_length = (0xf + 0x1) * read_data[0] + read_data[1]
            check_code = read_data[0] + read_data[1] + check_code
            print(f'帧长度Dec:{int(all_length)}')
            # print(f'协议版本Hex:{ser.read(1).hex()}')
            check_code += int(ser.read(1).hex(), 16)
            # print(f'帧类型Hex：{ser.read(1).hex()}')
            check_code += int(ser.read(1).hex(), 16)
            # print(f'字命令Hex：{ser.read(1).hex()}')
            check_code += int(ser.read(1).hex(), 16)

            read_data = ser.read(2)
            # print(f'read_data[0]:{read_data[0]},read_data[1]:{read_data[1]}')
            length = (0xf + 0x1) * read_data[0] + read_data[1]
            print(f'参数长度：{length}')
            check_code += read_data[0]
            check_code += read_data[1]
            # print(f'雷达转速值{int(ser.read(1).hex(), 16)}')
            check_code += int(ser.read(1).hex(), 16)
            # print(f'零点偏移量{int(ser.read(2).hex(), 16)}')
            check_code += int(ser.read(1).hex(), 16)
            check_code += int(ser.read(1).hex(), 16)
            # print(f'起始角度值{int(ser.read(2).hex(), 16)}')
            check_code += int(ser.read(1).hex(), 16)
            check_code += int(ser.read(1).hex(), 16)
            for i in range(int((length - 5) / 3)):
                # ser.read(1)  # 信号值
                check_code += int(ser.read(1).hex(), 16)
                # print(f'距离值：{int(ser.read(2).hex(), 16)}')
                check_code += int(ser.read(1).hex(), 16)
                check_code += int(ser.read(1).hex(), 16)
            print(f'校验码：{ser.read(2).hex()}')
            print(f'check_code:{hex(check_code)}')
            print('********************************************')


def read_data_print(ser):
    # print,用来方便查看
    while True:
        localtime = time.asctime(time.localtime(time.time()))
        # print(f'[时间：]{localtime}')
        data = ser.read(1).hex()
        # 寻找帧头
        if data == 'aa':
            all_length = int(ser.read(2).hex(), 16)
            print(f'帧长度Dec:{int(all_length)}')
            print(f'协议版本Hex:{ser.read(1).hex()}')
            print(f'帧类型Hex：{ser.read(1).hex()}')
            print(f'字命令Hex：{ser.read(1).hex()}')
            length = int(ser.read(2).hex(), 16)
            print(f'参数长度Dec：{length}')
            print(f'雷达转速值Dec：{int(ser.read(1).hex(), 16)}')
            print(f'零点偏移量Dec：{int(ser.read(2).hex(), 16)}')
            start_degree = int(ser.read(2).hex(), 16) * 0.01
            print(f'起始角度值Dec:{start_degree}°')
            number_of_degree_data = int((length - 5) / 3)
            for i in range(number_of_degree_data):
                ser.read(1)  # 信号值
                # print(f'距离值Dec：{int(ser.read(2).hex(), 16)*0.00025}m')
                print(
                    f'角度[{round(start_degree + 22.5 / number_of_degree_data * i, 4)}]'
                    f'距离值Dec：{round(int(ser.read(2).hex(), 16) * 0.025, 4)}cm')
            print(f'校验码：{ser.read(2).hex()}')
            # print(f'check_code:{hex(check_code)}')
            print('********************************************')


# ********************************************************************************************
def check_data_header(ser):
    # 用来检查当前的数据帧是否是我们要的
    data_header_0xaa = ser.read(1).hex()  # 帧头的校验码 ：Hex 0xaa
    # data_all_length = ser.read(2)  # 帧长度：正常的帧长度都是Dec 127
    ser.read(2)
    # data_header_protocol_version = ser.read(1)  # 协议类型：Hex 01
    ser.read(1)
    # data_header_frame_type = ser.read(1)  # 帧类型：Hex 61
    ser.read(1)
    # data_header_byte_command = ser.read(1)  # 字命令：Hex ad
    ser.read(1)
    data_parameter_length = int(ser.read(2).hex(), 16)  # 参数长度： Dec 119
    # radar_speed = ser.read(1)  # 雷达转速值，不用
    ser.read(1)
    # radar_offset = ser.read(2)  # 雷达偏移量，不用
    ser.read(2)
    start_degree = int(ser.read(2).hex(), 16)
    # number_of_degree_data = int((data_parameter_length - 5) / 3)# 固定为38
    if data_header_0xaa == 'aa' and data_parameter_length == 119:
        return True, start_degree
    else:
        return False, -1


def store_radar_data(conn_reading_radar_data_send, ser):
    numpy_array = np.zeros((16, 39))
    for i in range(16):
        try:
            check_data_header_result, start_degree = check_data_header(ser)  # 进行校验，并获取校验结果
            if check_data_header_result:
                numpy_array[i, -1] = start_degree
                for j in range(38):
                    ser.read(1)  # 信号值，无用
                    numpy_array[i, j] = int(ser.read(2).hex(), 16)  # 单位是0.25mm
                ser.read(2).hex()  # 校验码，无用
            else:
                # localtime = time.asctime(time.localtime(time.time()))
                # print(f'[时间：]{localtime}')
                # print("校验未通过！")
                return
        except ValueError:
            print('值为空')
            return
    # localtime = time.asctime(time.localtime(time.time()))
    # print(f'[ConnectSerial 141 时间：]{localtime}')
    conn_reading_radar_data_send.send(numpy_array)
    ser.reset_input_buffer()


def while_store_ladar_data(conn_reading_radar_data_send):
    ser = serial.Serial("/dev/ttyUSB0", 230400, timeout=0.5)  # 获取usb信息
    while True:
        store_radar_data(conn_reading_radar_data_send, ser)
        # print('存储成功')


# 读取雷达数据相关函数结束**************************88
# 绘制栅格图相关函数
# 500 * 500
def convey_radar_data(conn_reading_radar_data_recv):
    config = RaspberryServer.config()
    raspberry_server_radar_host = config.get('raspberry_server_setting',
                                             'raspberry_server_radar_host')  # 树莓派的ip地址
    raspberry_server_radar_port = config.getint('raspberry_server_setting',
                                                'raspberry_server_radar_port')  # 设置服务的端口号
    while True:
        latest_data = conn_reading_radar_data_recv.recv()
        dict_data = translate_to_raster(latest_data)
        raspberry_server_radar_socket = socket.socket()
        raspberry_server_radar_socket.connect((raspberry_server_radar_host, raspberry_server_radar_port))
        send_mess = bytes(str(dict_data), 'utf-8')
        msg = struct.pack('>I', len(send_mess)) + send_mess
        raspberry_server_radar_socket.sendall(msg)
        raspberry_server_radar_socket.close()  # 关闭连接


def translate_to_raster(numpy_array):
    # 分辨率为200*200 的栅格图，2.5m=2500mm = 0.25mm *100 *100格
    # 2.5 m = 250cm = 2500mm =0.25mm * 10000=0.25 * 40 *250 = 250 *10 mm= 250 *1 cm
    # 1格 = 1cm
    # 22.5/38 = 0.5921
    dict_data = {}
    for i in range(16):
        start_degree = numpy_array[i, -1] * 0.01
        for j in range(38):
            distance = numpy_array[i, j]
            if distance != 0:
                now_degree = (start_degree + j * 0.5921 - 90) * 2 * math.pi / 360
                draw_x = int(math.cos(now_degree) * distance / 40 + 0.5) + 250
                draw_y = int(math.sin(now_degree) * distance / 40 + 0.5) + 250
                if 0 <= draw_x < 500 and 0 <= draw_y < 500:
                    # 将点加入字典
                    if dict_data.get(draw_x) is None:
                        dict_data[draw_x] = {draw_y}
                    else:
                        dict_data.get(draw_x).add(draw_y)
    # print(f'block_in_10_cm:{block_in_10_cm}')
    return dict_data
