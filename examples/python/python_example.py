import paho.mqtt.client as mqtt
import random
import time

CLIENT_ID = "your device client_id"
USERNAME = "your emqx username"
PASSWORD = "your emqx password"
STREAM_ID_LIST = ["your device strame_ids"]
SERVER_URL = "127.0.0.1"
PORT = 1883

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

    # 连接成功之后订阅设备控制的topic
    if rc == 0:
        client.subscribe(f"/{USERNAME}/{CLIENT_ID}/#")
        # 订阅自己创建的其他设备topic:
        # client.subscribe(f"/{USERNAME}/{OTHER_CLIENT_ID}/#")
        # 订阅其他人分享给自己且有数据订阅权限的设备topic:
        # client.subscribe(f"/{OTHER_USERNAME}/{OTHER_CLIENT_ID}/#")

def on_message(client, userdata, msg):
    print(f"{msg.topic} -> {msg.payload}")

client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(username=USERNAME, password=PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(SERVER_URL, PORT, 60)
client.loop_start()

# 推送数据
while True:
    for i in STREAM_ID_LIST:
        client.publish(f"/{USERNAME}/{CLIENT_ID}/{i}", random.randint(0, 100))
    time.sleep(5)
