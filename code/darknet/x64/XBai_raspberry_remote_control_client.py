import multiprocessing
import socket
import sys
from multiprocessing.queues import Queue

from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import MyApp
import RadarData
import darknet_video
import time

netMain = None
metaMain = None
altNames = None


class CameraPageWindow(QWidget, MyApp.Ui_Form):

    def __init__(self, parent=None):
        super(CameraPageWindow, self).__init__(parent)
        self.config = darknet_video.readConfigFile()
        self.setupUi(self)
        self.slot_init()
        # 初始化socket
        self.control_signal_to_raspberry_socket = socket.socket()
        self.control_signal_socket_init()

    def slot_init(self):
        # 信号和槽连接
        self.buttonUp.pressed.connect(self.button_up_activity)
        self.buttonUp.clicked.connect(self.button_activity_stop)
        self.buttonDown.pressed.connect(self.button_down_activity)
        self.buttonDown.clicked.connect(self.button_activity_stop)
        self.buttonLeft.pressed.connect(self.button_left_activity)
        self.buttonLeft.clicked.connect(self.button_activity_stop)
        self.buttonRight.pressed.connect(self.button_right_activity)
        self.buttonRight.clicked.connect(self.button_activity_stop)
        self.buttonEmergencyStop.clicked.connect(self.button_activity_stop)

    def control_signal_socket_init(self):
        # 创建 socket 对象
        control_signal_to_raspberry_host = self.config.get('control_signal_setting',
                                                           "control_signal_to_raspberry_host")  # 获取本地主机名
        control_signal_to_raspberry_port = self.config.getint('control_signal_setting',
                                                              "control_signal_to_raspberry_port")  # 设置端口
        self.control_signal_to_raspberry_socket.bind(
            (control_signal_to_raspberry_host, control_signal_to_raspberry_port))  # 绑定端口
        self.control_signal_to_raspberry_socket.listen(5)  # 等待客户端连接

    def run_yolo(self):
        running_mode = self.config.get('darknet_video_setting', "running_mode")
        if running_mode == 'web':
            darknet_video.YOLO(False)
        elif running_mode == 'detected':
            darknet_video.YOLO(True)
        else:
            darknet_video.YOLO(True)

    def button_up_activity(self):
        self.showLogView.setText("press up")
        # 创建socket和web的传输
        connection_to_raspberry, addr = self.control_signal_to_raspberry_socket.accept()  # 建立和树莓派的socket通信
        # connection_to_raspberry.send(bytes(f'[controlSignal]:up', encoding='utf8'))
        connection_to_raspberry.send(bytes('up', encoding='utf8'))
        connection_to_raspberry.close()  # 关闭连接

    def button_down_activity(self):
        self.showLogView.setText("press down")
        connection_to_raspberry, addr = self.control_signal_to_raspberry_socket.accept()  # 建立和树莓派的socket通信
        connection_to_raspberry.send(bytes('down', encoding='utf8'))
        connection_to_raspberry.close()  # 关闭连接

    def button_left_activity(self):
        self.showLogView.setText("press left")
        connection_to_raspberry, addr = self.control_signal_to_raspberry_socket.accept()  # 建立和树莓派的socket通信
        connection_to_raspberry.send(bytes('left', encoding='utf8'))
        connection_to_raspberry.close()  # 关闭连接

    def button_right_activity(self):
        self.showLogView.setText("press right")
        connection_to_raspberry, addr = self.control_signal_to_raspberry_socket.accept()  # 建立和树莓派的socket通信
        connection_to_raspberry.send(bytes('right', encoding='utf8'))
        connection_to_raspberry.close()  # 关闭连接

    def button_activity_stop(self):
        self.showLogView.setText("stop")
        connection_to_raspberry, addr = self.control_signal_to_raspberry_socket.accept()  # 建立和树莓派的socket通信
        connection_to_raspberry.send(bytes('stop', encoding='utf8'))
        connection_to_raspberry.close()  # 关闭连接


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = CameraPageWindow(MainWindow)  # 注意把类名修改为myDialog
    # ui.setupUi(MainWindow)  myDialog类的构造函数已经调用了这个函数，这行代码可以删去
    MainWindow.setFixedSize(550, 640)
    MainWindow.show()
    # 多进程运行
    # queue_convey_detected_result = Queue()
    p_yolo = multiprocessing.Process(target=darknet_video.YOLO, args=(1,))
    p_yolo.start()
    multiprocessing.Process(target=RadarData.receive_radar_data_from_raspberry, args=()).start()
    sys.exit(app.exec_())
