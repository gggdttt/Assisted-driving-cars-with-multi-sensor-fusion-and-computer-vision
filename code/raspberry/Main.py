# 运行类
import _queue
import multiprocessing
import time
from multiprocessing import Pipe
from multiprocessing import Queue
import numpy
from RPi import GPIO

import ConnectSerial
import MotionModle
import RaspberryServer
import SmartDriving

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

if __name__ == '__main__':
    conn_control_signal_recv, conn_control_signal_send = Pipe(False)
    queue_detected_result = Queue()
    conn_reading_radar_data_recv, conn_reading_radar_data_send = Pipe(False)
    p_receive_control_signal = multiprocessing.Process(target=RaspberryServer.receive_control_signal,
                                                       args=(conn_control_signal_send,))
    p_receive_control_signal.start()
    p_receive_detected_result = multiprocessing.Process(target=RaspberryServer.receive_detected_result,
                                                        args=(queue_detected_result,))
    p_receive_detected_result.start()
    p_read_radar_data = multiprocessing.Process(target=ConnectSerial.while_store_ladar_data,
                                                args=(conn_reading_radar_data_send,))
    p_read_radar_data.start()
    p_convey_radar_data = multiprocessing.Process(target=ConnectSerial.convey_radar_data,
                                                  args=(conn_reading_radar_data_recv,))
    p_convey_radar_data.start()

    GPIO.setup(23, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(22, GPIO.IN)
    last_detected_result = False
    now_detected_result = False
    control_signal = 'stop'
    while True:
        try:
            now_detected_result = queue_detected_result.get_nowait()
        except _queue.Empty:
            now_detected_result = last_detected_result
        finally:
            if conn_control_signal_recv.poll(0.05):
                print(f'{time.asctime(time.localtime(time.time()))}:{now_detected_result}')
                control_signal = conn_control_signal_recv.recv()
                if control_signal == 'up':
                    MotionModle.forward()
                elif control_signal == 'down':
                    MotionModle.back()
                elif control_signal == 'right':
                    MotionModle.turn_right()
                elif control_signal == 'left':
                    MotionModle.turn_left()
                elif control_signal == 'stop':
                    MotionModle.stop()
            else:
                # 22 左 白 ,23 右  蓝 .24中 紫
                if control_signal == 'up':
                    # p
                    if now_detected_result:
                        # print(now_detected_result)
                        if not GPIO.input(24) or not GPIO.input(22) or not GPIO.input(23):
                            MotionModle.stop()
                    else:
                        # if not GPIO.input(24):

                        #     MotionModle.stop()
                        #     control_signal = 'stop'
                        # print(f'{time.asctime( time.localtime(time.time()) )}:{now_detected_result}')
                        if not GPIO.input(22):
                            MotionModle.turn_right()
                            time.sleep(0.4)
                            MotionModle.stop()
                            control_signal = 'stop'
                        elif not GPIO.input(23) or not GPIO.input(24):
                            MotionModle.turn_left()
                            time.sleep(0.4)
                            MotionModle.stop()
                            control_signal = 'stop'


