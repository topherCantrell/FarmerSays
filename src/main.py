import hdw_farmer_says as HDW
import farm_adafruit_io
import time

# Mapping of pins to animal name (for adafruit.io feed)
ANIMALS = {
    HDW.S_12_00  : 'Sheep',
    HDW.S_11_00  : 'Turkey',
    HDW.S_10_00  : 'Cat',
    HDW.S_9_00   : 'Bird',   
    HDW.S_8_00   : 'Cow',        
    HDW.S_7_00   : 'Pig',  
    HDW.S_6_00   : 'Rooster', 
    HDW.S_5_00   : 'Coyote',
    HDW.S_4_00   : 'Horse',   
    HDW.S_3_00   : 'Frog',     
    HDW.S_2_00   : 'Duck', 
    HDW.S_1_00   : 'Dog'
} 

def switch_changed(event):
    # TODO debounce these switches!
    animal = ANIMALS[event]
    #farm_adafruit_io.post_animal(farm_adafruit_io.FARM_CHRIS,animal)
    print(animal)
     
HDW.init(ANIMALS,switch_changed) 

HDW.set_motor(3000)
time.sleep(2)
HDW.set_motor(None) 

while(True):
    time.sleep(1)
    
'''
        speed = 2048
        
    set_motor(speed)
    
    time.sleep(2)
    
    set_motor(None)
'''