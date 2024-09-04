import time
# from machine import Pin
import machine
import urequests
from config import *
from blink import *

ENDPOINT = f'{REMOTE}/api/v2/write?orgID={ORG_ID}&bucket={BUCKET}'
headers = {
        "Authorization": f"Token {ACCESS_TOKEN}",
        "Content-Type": "text/plain; charset=utf-8",
        "Accept": "application/json"
}

# set debug True or False
debug = True

def postAPI(HOST,DATUM):
    BODY = f"{HOST} {DATUM}"
    print(BODY)
    response = urequests.post(ENDPOINT, headers=headers, data=f'{BODY}')# API POST postAPI('temp',HOST','temp=35')
    if response.status_code == 204:
        print("Data posted successfully")
        response.close()
        blink(3,0.1)
    else:
        print("Failed to post data")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        response.close()
        blink(10,0.5)
    return BODY
