import time

import machine

LED = machine.Pin("LED", machine.Pin.OUT)


def blink(SIG, DUR):
    LED.off()
    for i in range(SIG):
        time.sleep(DUR)
        LED.toggle()
    LED.off()
