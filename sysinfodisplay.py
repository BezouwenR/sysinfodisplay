#!/usr/bin/env python3

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from luma.core.error import DeviceNotFoundError
import os
import time
import signal
import sys
import socket

from PIL import ImageFont, ImageDraw

def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def getServiceStatus(service):
    if 0 == os.system("systemctl is-active --quiet " + service):
        return "OK"
    else:
        if 0 == os.system("systemctl is-failed --quiet " + service):
            return "Fail"
        else:
            return "N/A"

def signal_handler(sig, frame):
        print("\nApplication terminated with Ctrl+C.")
        sys.exit(0)

try:
    signal.signal(signal.SIGINT, signal_handler)
    serial = i2c(port=1, address=0x3C)
    device = ssd1306(serial, rotate=0)

    while True:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            font = ImageFont.truetype('./pixelmix.ttf', 10)
            ip = getIP()
            draw.text((5, 5), "IP: " + ip, fill="white", font=font)
            font = ImageFont.truetype('./pixelmix.ttf', 16)
            statusHomeBridge = getServiceStatus("homebridge")
            draw.text((5, 20), "HB: " + statusHomeBridge, fill="white", font=font)
            statusMQTT = getServiceStatus("mosquitto")
            draw.text((5, 42), "MQTT: " + statusMQTT, fill="white", font=font)
    sleep(1)
except DeviceNotFoundError:
    print("I2C mini OLED display not found.")
except SystemExit:
    print("Exiting...")
except:
    print("Unexpected error:", sys.exc_info()[0])