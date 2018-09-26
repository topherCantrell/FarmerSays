import hardware
import farm_stream
import time

# Mapping of pins to animal name (for feed)
ANIMALS = {
    4  : 'Sheep',   # 12:00
    5  : 'Turkey',  # 11:00
    6  : 'Cat',     # 10:00
    12 : 'Bird',    #  9:00    
    24 : 'Cow',     #  8:00        
    13 : 'Pig',     #  7:00   
    17 : 'Rooster', #  6:00
    23 : 'Coyote',  #  5:00
    22 : 'Horse',   #  4:00    
    25 : 'Frog',    #  3:00     
    20 : 'Duck',    #  2:00    
    16 : 'Dog'      #  1:00
} 

def switch_changed(event):
    # TODO debounce these switches!
    animal = ANIMALS[event]
    farm_stream.post_animal(farm_stream.FARM_CHRIS,animal)
    print(animal)
     
hardware.init_buttons(ANIMALS,switch_changed) 

while(True):
    time.sleep(1)