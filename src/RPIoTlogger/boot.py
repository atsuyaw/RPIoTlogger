# boot.py - - runs on boot-up
import network
import ubinascii
from blink import *
from config import *

# SSID =
# PASSWORD =
# HOSTNAME =
# REMOTE =
# ORG_ID =
# BUCKET =
# ACCESS_TOKEN =


wlan = network.WLAN(network.STA_IF)


def connect():
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to connect:")
        blink(5, 0.05)
        time.sleep(5)
    IP = wlan.ifconfig()[0]
    blink(3, 0.5)
    return IP


def setHost():
    host = network.hostname(HOSTNAME)
    return host


def getMac():
    rawMac = wlan.config("mac")
    MAC = str(ubinascii.hexlify(rawMac), "utf-8")
    return MAC


connect()
MAC = getMac()
