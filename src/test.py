import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#GPIO.add_event_detect(6, GPIO.BOTH, callback=my_callback)