import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


SWITCH_PINS = [
    4,  # 1
    5,  # 2
    6,  # 3
    12, # 4
         19, # 5    
    13, # 6    
    17, # 7
    23, # 8
    22, # 9
         21, # 10    
         20, # 11    
    16, # 12
    ] 
 
for s in SWITCH_PINS:
    GPIO.setup(s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    values = []
    for s in SWITCH_PINS:
        values.append(GPIO.input(s))
                    
    print(values)
    time.sleep(1)

#GPIO.add_event_detect(6, GPIO.BOTH, callback=my_callback)