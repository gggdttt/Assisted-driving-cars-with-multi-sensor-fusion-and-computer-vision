# 实现智能避障功能
# 数据来源：
# 1. @ ladar_data : 来自雷达的经过转化为字典的数据
# 2. @ control_signal: 通过socket 接收的来自客户端的控制信号
# 3. @ detected_result: 通过YOLO识别得到的图像结果
from ast import literal_eval
from queue import Empty

import MotionModle


def get_detected_data_from_pipe(conn_detected_result_recv, last_one_data):
    # while not queue.empty() or latest_data is None:
    #     latest_data = queue.get()
    # if not queue.empty():
    #     latest_data = queue.get()
    # if latest_data is None:
    #     return last_one_data
    # else:
    #     return latest_data
    try:
        latest_data = conn_detected_result_recv.recv()
        return latest_data
    except Empty:
        return last_one_data


def get_block_info_from_pipe(conn_radar_data_recv, last_one_data):
    try:
        latest_data = conn_radar_data_recv.recv()
        return latest_data
    except Empty:
        return last_one_data


def smart_driving(conn_radar_data_recv, conn_detected_result_recv, conn_control_signal_recv, queue_report_client=None):
    control_signal = 0
    detected_result = None
    block_info = None
    while True:
        block_info = get_block_info_from_pipe(conn_radar_data_recv, block_info)  # dic 格式
        detected_result = get_detected_data_from_pipe(conn_detected_result_recv, detected_result)  # dic格式
        # print(f'[SmartDriving:smart_driving]:line47:radar:{type(radar_data)}')
        # print(f'[SmartDriving:smart_driving]:line48:radar:{radar_data}')
        # print(f'[SmartDriving:smart_driving]:line47:detected_result:{type(detected_result)}')
        # print(f'[SmartDriving:smart_driving]:line48:detected_result:{detected_result}')
        control_signal = conn_control_signal_recv.recv()
        if control_signal is 1:
            # print(f'[SmartDriving:smart_driving]:line38:{radar_data}')
            control_signal = check_forward(block_info, detected_result)
        elif control_signal is 2:
            check_back(queue_report_client, block_info)
        elif control_signal is 3:
            check_left(queue_report_client, block_info)
        elif control_signal is 4:
            check_right(queue_report_client, block_info)
        elif control_signal is 0:
            pass


def check_forward(block_info, detected_result):
    MotionModle.init()
    # print(block_info)
    # print(detected_result)
    # if detected_result['hasPeople']
    if block_info['block_in_10_cm']:
        MotionModle.stop()
        return 0
    MotionModle.forward()
    return 1


def check_back(queue_report_client, radar_data):
    pass


def check_left(queue_report_client, radar_data):
    pass


def check_right(queue_report_client, radar_data):
    pass
