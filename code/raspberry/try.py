import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.on_disconnect = on_disconnect
client.connect('192.168.0.101', 1883, 600)  # 600为keepalive的时间间隔
client.subscribe('fifa', qos=0)
client.loop_forever()  # 保持连接
