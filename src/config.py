import machine

INT_TEMP_PIN = machine.ADC(4)

PH_PIN = machine.ADC(28) # for pH meas
PH_SPAN = 16 # max pH
PH_BASE = -1 # min pH
PH_REC_RANGE = 20 * pow(10,-3) # mA
PH_SHUNT_RES = 150 # ohm
PH_COEFF = PH_SPAN / (PH_REC_RANGE * PH_SHUNT_RES)

VOL_PIN = machine.ADC(27)
VOL_RES1 = 6.6 # Part Res for vol meas
VOL_RES2 = 3.3
VOL_MAX = 36

CUR_PIN = machine.ADC(26)
CUR_RES1 = 6.6 # Part Res for vol meas
CUR_RES2 = 3.3
CUR_MAX = 3

ONETEMP_PIN = machine.Pin(22)

# Set secrets
SSID = ""
PASSWORD = ""

# InfluxDB
REMOTE = ""# Host name and port
ORG_ID = ""
BUCKET = ""
ACCESS_TOKEN = ""

