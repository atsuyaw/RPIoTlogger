from config import *
from intTemp import *
from OneTemp import *
from postAPI import *
from rawADC import *
# SSID =
# PASSWORD =
# HOSTNAME =
# REMOTE =
# ORG_ID =
# BUCKET =
# ACCESS_TOKEN =
from wifi import *

print("IP: " + connect())
MAC = getMac()

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
    utime.sleep(60)
