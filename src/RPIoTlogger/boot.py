import binascii
import time

import machine
import network


import config
# class Config:
    AP = {"Wokwi-GUEST": "PW"}


# class Remote:
#     ENDPOINT =
#     ORG_ID =
#     BUCKET =
#     ACCESS_TOKEN =

nic = network.WLAN(network.STA_IF)
nic.active(True)


print("Found APs:")
print("ssid, bssid, channel, RSSI, security, hidden")
time.sleep(0.1)


def wlan_scan(_nic):
    # found_ap = nic.scan()
    found_ap = sorted(_nic.scan(), key=lambda _ap: _ap[3], reverse=True)  # RSSI

    for i in found_ap:
        # print(i[0].decode())
        print(i)
        time.sleep(0.1)


wlan_scan(nic)


interval = 0.5
delay = 0
time_limit = 5.0

for _ap in Config.AP:
    print("Connecting to", _ap, end="")
    _pw = Config.AP[_ap]
    nic.connect(_ap, _pw)

    while not nic.isconnected() and nic.status() >= 0:
        print(".", end="")
        # blink(5, 0.05)# Connecting...TODO
        time.sleep(interval)
        delay += interval

        if delay > time_limit:
            nic.disconnect()
            raise TimeoutError

# if nic.isconnected():
# blink(3, 0.5)# Connected TODO
print("Connected:", nic.status())


print(network.hostname())

uid = machine.unique_id()
print(str(binascii.hexlify(uid), "utf-8"))


def get_mac():
    _raw_mac = nic.config("mac")
    _mac = str(binascii.hexlify(_raw_mac), "utf-8")
    return _mac


get_mac()  # TODO: rm later
