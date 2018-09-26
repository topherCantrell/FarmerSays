import RPi.GPIO as GPIO

def init_buttons(pins, callback=None):
    """ Initialize buttons
    
    For a list of pins, configure the pins for input and register
    a callback function to be called when the button is pressed.
    
    Parameters:
    
        pins: list of pins
        callback: the function to call when any switch is pressed
    
    """
    
    GPIO.setmode(GPIO.BCM)
    for s in pins:
        GPIO.setup(s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if callback:
            GPIO.add_event_detect(s, GPIO.RISING, callback=callback)  
