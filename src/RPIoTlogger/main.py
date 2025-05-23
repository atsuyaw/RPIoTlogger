# from blink import *
import time
from secrets import *

import machine

# from version import *
import network
import requests
import ubinascii

int_led = machine.Pin(25, machine.Pin.OUT)
led1 = machine.Pin(2, machine.Pin.OUT)
led2 = machine.Pin(3, machine.Pin.OUT)
sw1 = machine.Pin(10, machine.Pin.IN, machine.Pin.PULL_UP)

int_led.on()
led1.off()
led2.off()


def blink(led, sig, dur):
    for i in range(2 * sig):
        led.toggle()
        time.sleep(dur)


wlan = network.WLAN(network.STA_IF)


def connect():
    wlan.deinit()
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected() and wlan.status() >= 0:
        blink(led1, 5, 0.1)
        print("Waiting to connect:")
        time.sleep(5)
    IP = wlan.ifconfig()[0]
    print(IP)
    return IP


def getMac():
    rawMac = wlan.config("mac")
    MAC = str(ubinascii.hexlify(rawMac), "utf-8")
    return MAC


MAC = getMac()

while not wlan.isconnected():
    connect()
    time.sleep(5)

led1.on()

led2.on()
import mip

mip.install(
    "https://raw.githubusercontent.com/endail/hx711-pico-mpy/refs/heads/main/src/hx711.py"
)
led2.off()

from hx711 import *

hx = hx711(machine.Pin(18), machine.Pin(19))
hx.set_power(hx711.power.pwr_up)
hx.set_gain(hx711.gain.gain_128)
hx.set_power(hx711.power.pwr_down)
hx711.wait_power_down()
hx.set_power(hx711.power.pwr_up)
hx711.wait_settle(hx711.rate.rate_10)


def get_raw_hx():
    raw_hx = hx.get_value()
    if raw_hx := hx.get_value_timeout(250000):
        return raw_hx
    if raw_hx := hx.get_value_noblock():
        return raw_hx


def hx_kg(ins):
    ins = get_raw_hx()
    weight_kg = (ins * 0.00186277 + 1008.6124) / 1000
    return weight_kg


# >>> hxa = get_raw_hx()
# >>> hx_kg(hxa)

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)


def get_int_temp():
    result = []
    for i in range(10):
        reading = sensor_temp.read_u16() * conversion_factor
        sensorTemp = 27 - (reading - 0.706) / 0.001721
        print(sensorTemp)
        time.sleep_ms(10)
        result.append(sensorTemp)
    return result


def ave(ins):
    try:
        list = ins
        avg = sum(list) / len(list)
        return avg
    except IndexError:
        return -273.15


import ds18x20
import onewire

one_temp = machine.Pin(22)


def get_one_temp(ins):
    ow = onewire.OneWire(ins)  #  1-Wire path
    ds = ds18x20.DS18X20(ow)  #  ds18x20 class instance
    #  get rom code
    roms = ds.scan()  #  64bit roms <class 'list'>
    print("roms=", roms)
    try:
        rom = roms[0]  #  Set [0] because there is only DS18B20 for 1-Wire
        result = []
        for i in range(10):
            temp = ds.convert_temp()  #  Store temp datum in the scratchpad
            time.sleep(1)
            temp = ds.read_temp(rom)  #  Get Celsius temp
            print(temp)
            time.sleep_ms(10)
            result.append(temp)
        return result
    except IndexError:
        pass


# got = get_one_temp(one_temp)


def get_raw_adc(PIN, COEFF, SHIFT):
    VIN = machine.ADC(PIN)
    CONV = 1 / 65535
    result = []
    for i in range(100):
        RAWV = VIN.read_u16() * CONV * COEFF + SHIFT
        # print(RAWV)
        time.sleep_ms(10)
        result.append(RAWV)
    return result


ENDPOINT = f"http://{REMOTE}/api/v2/write?orgID={ORG_ID}&bucket={BUCKET}"
HEADER = {
    "Authorization": f"Token {ACCESS_TOKEN}",
    "Content-Type": "text/plain; charset=utf-8",
    "Accept": "application/json",
}

# set debug True or False
debug = True


def post(data):
    body = f"{HOST} {data}"
    print(body)
    try:
        res = requests.post(
            ENDPOINT, headers=HEADER, data=f"{body}"
        )  #  API POST postAPI('temp',HOST','temp=35')
        if res.status_code >= 400:
            print(res.text)
        code = res.status_code
        res.close()
        return code
    except OSError as e:
        print(f"OSError: " + f"{e}")
        return e


while True:
    int_temp = get_int_temp()
    int_temp = ave(int_temp)

    ADC_CUR_PIN = 1
    COEFF_CUR = 6.7625
    SHIFT_CUR = 0.0118
    CUR = aveRawV(ADC_CUR_PIN, COEFF_CUR, SHIFT_CUR)
    ADC_VOL_PIN = 0
    COEFF_VOL = 81.331
    SHIFT_VOL = 0.1398
    VOL = aveRawV(ADC_VOL_PIN, COEFF_VOL, SHIFT_VOL)
    ONE_TEMP_PIN = 12
    ONE_TEMP = aveOneTemp(ONE_TEMP_PIN)
    WEIGHT = hx.get_value()
    data = (
        f"int_temp={INT_TEMP},"
        + f"one_temp={ONE_TEMP},"
        + f"current={CUR},"
        + f"voltage={VOL},"
        + f"weight={WEIGHT},"
        + f'app="{__app__}",'
        + f'ver="{__version__}"'
    )
    postAPI(MAC, data)
    time.sleep(30)
    post(data)
