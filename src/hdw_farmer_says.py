import RPi.GPIO as GPIO

import smbus
import time

# Switch pins named by their position on the clock facing the toy
S_12_00 = 4
S_11_00 = 5
S_10_00 = 6
S_9_00  = 12
S_8_00  = 24
S_7_00  = 13 
S_6_00  = 17
S_5_00  = 23
S_4_00  = 22
S_3_00  = 25
S_2_00  = 20
S_1_00  = 16

def init(pins, callback=None):
    """ Initialize the hardware
    
    For a list of pins, configure the pins for input and register
    a callback function to be called when the button is pressed.
    
    Initialize the motor driver.
    
    Parameters: 
    
        pins: list of pins
        callback: the function to call when any switch is pressed
    
    """
   
    global _bus,_address
     
    _bus = smbus.SMBus(1)
    _address = 0x60

    _bus.write_byte_data(_address,0,1)    # ALLCALL enabled (optional)
    time.sleep(0.005)                     # Wait for oscillator
        
    GPIO.setmode(GPIO.BCM)
    for s in pins:
        GPIO.setup(s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        if callback:
            GPIO.add_event_detect(s, GPIO.RISING, callback=callback,bouncetime=1000)  

def set_motor(speed):
    """ Set the motor speed
    
    Positive values are clockwise. Negative values are counterclockwise.
    Pass 'None' to release the motor.    
    
    Parameters:
        speed: 0 to 4095 (positive or negative) or None
    """
                
    if speed == None:
        # Release the motor
        _set_pwm(_MOTORS[0],0,0)
        _set_bool(_MOTORS[1],False)
        _set_bool(_MOTORS[2],False)            
    elif speed<0:            
        # Counterclockwise
        _set_pwm(_MOTORS[0],0,-speed)
        _set_bool(_MOTORS[1],False)
        _set_bool(_MOTORS[2],True)  
    else:
        # Clockwise
        _set_pwm(_MOTORS[0],0,speed)
        _set_bool(_MOTORS[2],False)
        _set_bool(_MOTORS[1],True)  

# This maps output channels to motors. There are 3 channels per motor.
# The first channel is the motor's PWM.
# The second and third channels are the boolean directions.
_MOTORS = (8,9,10)

def _set_pwm(channel, on_cnt, off_cnt):
    global _bus, _address
    # Each channel has 4 registers (a word for ON time and a word for OFF time)
    _bus.write_byte_data(_address, 6+channel*4,  on_cnt & 0xFF)
    _bus.write_byte_data(_address, 7+channel*4,  on_cnt >> 8)
    _bus.write_byte_data(_address, 8+channel*4, off_cnt & 0xFF)
    _bus.write_byte_data(_address, 9+channel*4, off_cnt >> 8)

def _set_bool(channel, value):
    # Set the output pin to a solid value -- 1 or 0
    if value:
        _set_pwm(channel,4096,0)
    else:
        _set_pwm(channel,0,4096)