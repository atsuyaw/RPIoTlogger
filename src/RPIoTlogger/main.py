import ds18x20
import onewire
import time
import machine
import requests
from blink import *

from config import *
# SSID =
# PASSWORD =
# HOSTNAME =
# REMOTE =
# ORG_ID =
# BUCKET =
# ACCESS_TOKEN =


def getRawV(PIN, VMAX):
    VIN = machine.ADC(PIN)
    conversion_factor = VMAX / 65535
    result = []
    for i in range(10):
        RAWV = VIN.read_u16() * conversion_factor
        time.sleep_ms(10)
        result.append(RAWV)
    return result


def aveRawV(PIN, VMAX):
    list = getRawV(PIN, VMAX)
    avg = sum(list) / len(list)
    return avg



sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)


def get_sensor_temp():
    result = []
    for i in range(10):
        reading = sensor_temp.read_u16() * conversion_factor
        sensorTemp = 27 - (reading - 0.706) / 0.001721
        print(sensorTemp)
        time.sleep_ms(10)
        result.append(sensorTemp)
    return result


def aveIntTemp():
    list = get_sensor_temp()
    print(list)
    avg = sum(list) / len(list)
    # print("avg: " + str(avg))
    return avg



def getOneTemp(PIN):
    ow = onewire.OneWire(machine.Pin(PIN))  #  1-Wire path
    ds = ds18x20.DS18X20(ow)  #  ds18x20 class instance
    #  get rom code
    roms = ds.scan()  #  64bit roms <class 'list'>
    print("roms=", roms)
    rom = roms[0]  #  Set [0] because there is only DS18B20 for 1-Wire
    result = []
    for i in range(10):
        temp = ds.convert_temp()  #  Store temp datum in the scratchpad
        time.sleep_ms(750)
        temp = ds.read_temp(rom)  #  Get Celsius temp
        print(temp)
        time.sleep_ms(10)
        result.append(temp)
    return result


def aveOneTemp(PIN):
    list = getOneTemp(PIN)
    print(list)
    avg = sum(list) / len(list)
    # print("avg: " + str(avg))
    return avg




ENDPOINT = f"{REMOTE}/api/v2/write?orgID={ORG_ID}&bucket={BUCKET}"
headers = {
    "Authorization": f"Token {ACCESS_TOKEN}",
    "Content-Type": "text/plain; charset=utf-8",
    "Accept": "application/json",
}

# set debug True or False
debug = True


def postAPI(HOST, DATUM):
    BODY = f"{HOST} {DATUM}"
    print(BODY)
    response = requests.post(
        ENDPOINT, headers=headers, data=f"{BODY}"
    )  #  API POST postAPI('temp',HOST','temp=35')
    if response.status_code == 204:
        print("Data posted successfully")
        response.close()
        blink(3, 0.1)
    else:
        print("Failed to post data")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        response.close()
        blink(10, 0.5)
    return BODY




while True:
    INT_TEMP = aveIntTemp()
    RAW_V_PIN = 0
    RAW_VMAX = 41.6  #  Conversion factor for ADC0
    RAW_V = aveRawV(RAW_V_PIN, RAW_VMAX)
    RAW_VB_PIN = 1
    RAW_VB_MAX = 1.21  #  Conversion factor for ADC1
    RAW_VB = aveRawV(RAW_VB_PIN, RAW_VB_MAX)
    ONE_TEMP_PIN = 12
    ONE_TEMP = aveOneTemp(ONE_TEMP_PIN)
    DATUM = (
        f"int_temp={INT_TEMP},"
        + f"one_temp={ONE_TEMP},"
        + f"voltage={RAW_V},"
        + f"rawVmax={RAW_VMAX},"
        + f"current={RAW_VB},"
        + f"rawVBmax={RAW_VB_MAX},"
        + f"ver={VER}"
    )
    postAPI(MAC, DATUM)
    time.sleep(60)
