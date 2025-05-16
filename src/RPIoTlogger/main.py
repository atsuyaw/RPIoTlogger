APP = 'RPIoTlogger'
VER = '0.2.0'
#
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
    ADC_CUR_PIN = 1
    COEFF_CUR = 6.7625
    SHIFT_CUR = 0.0118
    CUR = aveRawV(ADC_CUR_PIN,COEFF_CUR,SHIFT_CUR)
    ADC_VOL_PIN = 0
    COEFF_VOL = 81.331
    SHIFT_VOL = 0.1398
    VOL = aveRawV(ADC_VOL_PIN,COEFF_E,SHIFT_E)
    ONE_TEMP_PIN = 12
    ONE_TEMP = aveOneTemp(ONE_TEMP_PIN)
    DATUM = f'int_temp={INT_TEMP},'\
            + f'one_temp={ONE_TEMP},'\
            + f'current={CUR}'\
            + f'voltage={VOL},'\
            + f'app={APP},'\
            + f'ver={VER}'
    postAPI(MAC, DATUM)
    utime.sleep(30)
