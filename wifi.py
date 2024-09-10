# https://qiita.com/smart_agri_lab/items/0a63b7cf0ad71e2015ba
import network
import ubinascii
from config import *
from blink import *

wlan = network.WLAN(network.STA_IF)


def connect():
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect:")
        blink(5, 0.05)
        time.sleep(5)
    IP = wlan.ifconfig()[0]
    # return ip
    # print(f'IP: {ip}')
    print('Hello world')
    blink(3, 0.5)
    return IP


def setHost():
    host = network.hostname(HOSTNAME)
    return host


def getMac():
    rawMac = wlan.config('mac')
    MAC = str(ubinascii.hexlify(rawMac),'utf-8')
    return MAC

