# 控制小车运动的模块
# 写了几个控制小车运动模块的函数
# 小车的运动可能会和接线的方法有关
# BCM编码中，pin40对应21，pin 38对应20，pin31对应6 pin29对应 5
# pin40接L298N电机驱动模块的4号In脚 ，pin38接3号In脚，pin31接2，pin29接1

import RPi.GPIO as GPIO


# led1 = LED(21)  # pin40
# led2 = LED(20)  # pin39
# led3 = LED(6)  # pin31
# led4 = LED(5)  # pin29
def init():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)


def forward():
    GPIO.output(6, GPIO.HIGH)  # LED(6).on()
    GPIO.output(5, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.HIGH)


def turn_left():
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.HIGH)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)


def turn_right():
    GPIO.output(21, GPIO.HIGH)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)


def back():
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(20, GPIO.HIGH)
    GPIO.output(21, GPIO.LOW)


def stop():
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)
    GPIO.output(21, GPIO.LOW)

# def check_gpio(queue):
#     # 可以在这里面send 到主机
#     while True:
#
# print("我最喜欢普林杰了！")
