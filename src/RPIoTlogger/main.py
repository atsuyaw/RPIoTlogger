# from blink import *
import time
from config import *
from secrets import *

import machine

# from version import *
from network import WLAN
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

# while not wlan.isconnected():
#     connect()
#     time.sleep(5)

led1.off()

led2.on()
try:
    import hx7111
except ImportError:
    import mip
    mip.install(
        "https://raw.githubusercontent.com/endail/hx711-pico-mpy/refs/heads/main/src/hx711.py"
    )
led2.off()


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



def avg(ins, lim, dur):
    r = []
    for i in range(lim):
        r.append(ins)
        time.sleep(dur)
    try:
        avg = sum(r) / len(r)
        return avg
    except IndexError:
        return


import ds18x20
import onewire


def get_onetemp(ins):
    ow = onewire.OneWire(ins)  #  1-Wire path
    ds = ds18x20.DS18X20(ow)  #  ds18x20 class instance
    roms = ds.scan()  #  64bit roms <class 'list'>
    rom = roms[0]  #  Set [0] because there is only DS18B20 for 1-Wire
    temp = ds.convert_temp()  #  Store temp datum in the scratchpad
    time.sleep(1)
    temp = ds.read_temp(rom)  #  Get Celsius temp
    return temp


def meas_adc(ins):
    volt = ins.read_u16() / 65535 * 3.3
    return volt

ENDPOINT = f"http://{REMOTE}/api/v2/write?orgID={ORG_ID}&bucket={BUCKET}"
HEADER = {
    "Authorization": f"Token {ACCESS_TOKEN}",
    "Content-Type": "text/plain; charset=utf-8",
    "Accept": "application/json",
}


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
        raise RuntimeError(code)
    except OSError as e:
        print(f"OSError: " + f"{e}")
        return e

# TODO: Switch for behavior
# sw1.value() == 1


while True:
    led2.off()
    if raw_int_temp := 27 - ( meas_adc(INT_TEMP_PIN) - 0.706 ) / 0.001721:
        dec_int_temp = "int_temp=" + f"{avg(raw_int_temp, 5, 0.01)},"
    else:
        dec_int_temp = ""
    ph = avg(meas_adc(PH_PIN),5,0.1) * PH_COEFF + PH_BASE
    dec_ph = "pH=" + f"{ph},"
    vol = avg(meas_adc(VOL_PIN),5,0.1) / VOL_RES2 * (VOL_RES1 + VOL_RES2) * VOL_MAX
    dec_vol = "voltage=" + f"{vol},"
    cur = avg(meas_adc(CUR_PIN),5,0.1) / CUR_RES2 * (CUR_RES1 + CUR_RES2) * CUR_MAX
    dec_cur = "current=" + f"{cur},"
    if raw_temp := get_onetemp(ONETEMP_PIN):
        dec_temp = "temp=" + f"{avg(raw_temp, 5, 0)},"
    else:
        dec_temp = ""
    if raw_weight := ( get_raw_hx() * 0.00186277 + 1008.6124) / 1000:
        dec_weight = "weight=" + f"{avg(raw_weight,5,0.1)},"
    else:
        dec_weight = ""
    
    data = (
        dec_int_temp + dec_ph + dec_vol + dec_cur + dec_temp + dec_weight
        + f'APP="{__app__}",'
        + f'VER="{__version__}"'
    )
    time.sleep(1)
    try:
        post(data)
    except:
        led2.on()
