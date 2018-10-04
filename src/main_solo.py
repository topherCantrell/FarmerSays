import time
import threading

import hdw_farmer_says as HDW # Switches and motor
import farm_audio as AUD      # Audio files

def switch_changed(event):    
    # Two threads: one to manage the audio and one to run the motor.
    animal = ANIMALS[event]    
    t = threading.Thread(target=AUD.prompt_and_play,args=(animal,))
    t.start()
    t = threading.Thread(target=HDW.spin_motor)
    t.start()     

# Mapping of pins to animal name (for audio files)
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
     
HDW.init(switch_changed) 

# Tell the user we are ready (it takes a few seconds
# to initialize pygame and load the sounds).
AUD.play('Rooster')
HDW.spin_motor()

while(True):
    time.sleep(1)
