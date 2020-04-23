# # BCM编码中，pin40对应21，pin 38对应20，pin31对应6 pin29对应 5
# from gpiozero import LED
# from time import sleep
# led1 = LED(21)
# led2 = LED(6)
# print("我最喜欢普林杰了！")
# while True:
#     led1.on()
#     # sleep(5)
#     # led1.off()
#     led2.on()
#     # sleep(5)
#     # led2.off()
first_name = 'Fan'
name = 'wenjie'
msg = f'{first_name} {name} is a hero'

print(msg.title())
