from wifi import *
from intTemp import *
from OneTemp import *
from pulseCnt import *
from rawADC import *
from postAPI import *
import network
import time

print('IP: '+ connect())
print('Host name: ' + setHost())
HOST = network.hostname()

while True:
    INT_TEMP = aveIntTemp()
    RAW_V_PIN = 0
    RAW_VMAX = 41.6# Conversion factor for ADC0
    RAW_V = aveRawV(RAW_V_PIN,RAW_VMAX)
    RAW_VB_PIN = 1
    RAW_VB_MAX = 1.21# Conversion factor for ADC1
    RAW_VB = aveRawV(RAW_VB_PIN,RAW_VB_MAX)
    ONE_TEMP_PIN = 12
    ONE_TEMP = aveOneTemp(ONE_TEMP_PIN)
    DATUM = f'int_temp={INT_TEMP},one_temp={ONE_TEMP},voltage={RAW_V},rawVmax={RAW_VMAX},current={RAW_VB},rawVBmax={RAW_VB_MAX},ver={APP}{VER}'
    postAPI(HOST,DATUM)
    sleep(60)
