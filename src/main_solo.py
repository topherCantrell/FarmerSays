import time
import threading

import hdw_farmer_says as HDW # Switches and motor
import farm_audio as AUD      # Audio files

def spin_motor():   
    # Start fast to get the motor going then fade
    HDW.set_motor(3000)
    time.sleep(0.5)
    HDW.set_motor(1500)
    time.sleep(1)
    HDW.set_motor(800)
    time.sleep(1)
    HDW.set_motor(None)

def switch_changed(event):    
    # Two threads: one to manage the audio and one to run the motor.
    animal = ANIMALS[event]    
    t = threading.Thread(target=AUD.prompt_and_play,args=(animal,))
    t.start()
    t = threading.Thread(target=spin_motor)
    t.start()     

# Mapping of pins to animal name (for audio files)
ANIMALS = {
    HDW.S_12_00  : 'sheep',
    HDW.S_11_00  : 'turkey',
    HDW.S_10_00  : 'cat',
    HDW.S_9_00   : 'bird',   
    HDW.S_8_00   : 'cow',        
    HDW.S_7_00   : 'pig',  
    HDW.S_6_00   : 'rooster', 
    HDW.S_5_00   : 'coyote',
    HDW.S_4_00   : 'horse',   
    HDW.S_3_00   : 'frog',     
    HDW.S_2_00   : 'duck', 
    HDW.S_1_00   : 'dog'
} 
     
HDW.init(ANIMALS,switch_changed) 

# Tell the user we are ready (it takes a few seconds
# to initialize pygame and load the sounds).
AUD.play('rooster')
spin_motor()

while(True):
    time.sleep(1)
