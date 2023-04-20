import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    
    # return commPort
    return 'COM6'

if getPort() != "None":
    ser = serial.Serial(port= getPort(), baudrate= 115200)
    print(ser)


def processData(data, client):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(",")
    
    print(splitData)
    for i in range(0, len(splitData)):
        splitStr = splitData[i].split(":")
        
        if splitStr[0] == "temp":
            if temp != splitStr[1]:
                temp = splitStr[1]
                client.publish("pasic-smart-office.temperature", temp)

        elif splitStr[0] == "humi":
            if humi != splitStr[1]:
                humi = splitStr[1]
                client.publish("pasic-smart-office.humidity", humi)
            
        elif splitStr[0] == "lux":
            if light != splitStr[1]:
                light = splitStr[1]
                client.publish("pasic-smart-office.brightness", light)
    
    writeData("!ACK#")
        
mess = ""
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1], client)
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
                
def writeData(data):
    ser.write(str(data).encode())                