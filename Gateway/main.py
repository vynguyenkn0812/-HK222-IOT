print("Hello Adafruit!!!")
import sys
import random
import time
from Adafruit_IO import MQTTClient
import cv2
from read_serial import *
from simple_ai import *

AIO_FEED_ID = ["iot-hk222.light", "iot-hk222.pump"]
AIO_USERNAME = "vynguyen08122002"
AIO_KEY = "aio_jTpa00iRWo7ACInoo8sMTJ1I7Pr8"

def connected(client):
    print("Ket noi thanh cong...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)
    
def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong...")
    
def disconnected(client):
    print("Ngat ket noi...")
    sys.exit(1)
    
def message(client, feed_id, payload):
    print("Nhan du lieu tu " + feed_id + " :" + payload)
    if feed_id == "iot-hk222.light":
        if payload == "1":
            writeData("!BON#")
        elif payload == "0":
            writeData("!BOFF#")
            
    elif feed_id == "iot-hk222.pump":
        if payload == "1":
            writeData("!PON#")
        elif payload == "0":
            writeData("!POFF#")
    
client = MQTTClient(AIO_USERNAME, AIO_KEY)
# call back with function pointer
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe

client.connect()
client.loop_background()

counter = 5
sensor_type = 0
prev_image = ""

while True:
    counter = counter - 1
    if counter <= 0:
        counter = 5
        readSerial(client)
        # if sensor_type == 0:
        #     temp = random.randint(0, 50)
        #     print("Cap nhat nhiet do: ", temp)
        #     client.publish("iot-hk222.temperature", temp)
        #     sensor_type = 1
        # elif sensor_type == 1:
        #     humi = random.randint(0, 100)
        #     print("Cap nhat do am: ", humi)
        #     client.publish("iot-hk222.humidity", humi)
        #     sensor_type = 2
        # elif sensor_type == 2:
        #     brightness = random.randint(0, 500)
        #     print("Cap nhat anh sang: ", brightness)
        #     client.publish("iot-hk222.brightness", brightness)
        #     sensor_type = 0
    ai_image = image_detection()
    
    if prev_image != ai_image:
        print("AI Detection result: ", ai_image)
        client.publish("iot-hk222.ai", ai_image)
        prev_image = ai_image
    
    time.sleep(1)