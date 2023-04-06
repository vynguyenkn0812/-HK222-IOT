print("Hello Adafruit!!!")
import sys
import random
import time
import serial.tools.list_ports
from Adafruit_IO import MQTTClient

AIO_FEED_ID = ["iot-hk222.light", "iot-hk222.pump"]
AIO_USERNAME = "vynguyen08122002"
AIO_KEY = "aio_jbbh17Y4DOch5E5IMUwgx3U6nwxS"

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

# def getPort():
#     ports = serial.tools.list_ports.comports()
#     N = len(ports)
#     commPort = "None"
#     for i in range(0, N):
#         port = ports[i]
#         strPort = str(port)
#         if "USB Serial Device" in strPort:
#             splitPort = strPort.split(" ")
#             commPort = (splitPort[0])
    
#     return commPort

# ser = serial.Serial ( port = getPort() , baudrate =115200)

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

while True:
    counter = counter - 1
    if counter <= 0:
        counter = 5
        if sensor_type == 0:
            temp = random.randint(0, 50)
            print("Cap nhat nhiet do: ", temp)
            client.publish("iot-hk222.temperature", temp)
            sensor_type = 1
        elif sensor_type == 1:
            humi = random.randint(0, 100)
            print("Cap nhat do am: ", humi)
            client.publish("iot-hk222.humidity", humi)
            sensor_type = 2
        elif sensor_type == 2:
            brightness = random.randint(0, 500)
            print("Cap nhat anh sang: ", brightness)
            client.publish("iot-hk222.brightness", brightness)
            sensor_type = 0
        
    time.sleep(1)
    
    # press Esc to escape program
    # Listen to the keyboard for presses.
    keyboard_input = cv2.waitKey(1)

    # 27 is the ASCII for the esc key on your keyboard.
    if keyboard_input == 27:
        break
