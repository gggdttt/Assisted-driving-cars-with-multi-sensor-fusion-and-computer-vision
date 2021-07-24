import datetime
import socket
import struct
import time
import darknet_video
import numpy as np
import cv2 as cv


def receive_radar_data_from_raspberry():
    config = darknet_video.readConfigFile()
    # 创建 socket 对象
    receive_radar_data_from_raspberry_socket = socket.socket()
    receive_radar_data_from_raspberry_host = config.get('radar_setting',
                                                        "raspberry_server_radar_host")  # 获取本地主机名
    receive_radar_data_from_raspberry_port = config.getint('radar_setting',
                                                           "raspberry_server_radar_port")  # 设置端口
    receive_radar_data_from_raspberry_socket.bind(
        (receive_radar_data_from_raspberry_host, receive_radar_data_from_raspberry_port))  # 绑定端口
    receive_radar_data_from_raspberry_socket.listen(5)
    while True:
        numpy_draw = np.zeros((500, 500, 3), np.uint8)
        point_size = 1
        point_color = (0, 0, 255)  # BGR
        thickness = 0  # 可以为 0 、4、8
        connection, address = receive_radar_data_from_raspberry_socket.accept()
        raw_msglen = connection.recv(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # print(f'{datetime.datetime.now()}:{msglen}')
        data = bytearray()
        while len(data) < msglen:
            packet = connection.recv(msglen - len(data))
            if not packet:
                return None
            data.extend(packet)
        connection.close()
        # print(f'{datetime.datetime.now()}:{data}')
        # try:
        dict_data = eval(data)
        for key in dict_data:
            for value in dict_data[key]:
                cv.circle(numpy_draw, (int(key), int(value)), point_size, point_color, thickness)
        # 画矩形（车）
        cv.rectangle(numpy_draw, (251, 247), (263, 277), (255, 255, 0), cv.FILLED)
        cv.namedWindow("image")
        cv.imshow('image', numpy_draw)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        cv.waitKey(100)  # 显示 10000 ms 即 10s 后消失


def route_path(numpy_draw, dict_data):
    pass


if __name__ == "__main__":
    receive_radar_data_from_raspberry()
    # numpy_draw = np.zeros((500, 500, 3), np.uint8)
    # point_size = 1
    # point_color = (0, 0, 255)  # BGR
    # thickness = 4  # 可以为 0 、4、8
    # cv.circle(numpy_draw, (100, 50), point_size, point_color, thickness)
    # cv.namedWindow("image")
    # cv.imshow('image', numpy_draw)
    # cv.waitKey(10000)  # 显示 10000 ms 即 10s 后消失
