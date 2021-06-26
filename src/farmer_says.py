import threading
import time

import RPi.GPIO as GPIO
import pygame
import smbus

pygame.mixer.init()


class FarmerSays:
    '''Interface to the "Farmer Says" hardware'''
        
    _PIN_NAMES = {
        4 : '12_oclock',
        5 : '11_oclock',
        6 : '10_oclock',
        12 : '9_oclock',
        24 : '8_oclock',
        13 : '7_oclock' ,
        17 : '6_oclock',
        23 : '5_oclock',
        22 : '4_oclock',
        25 : '3_oclock',
        20 : '2_oclock',
        16 : '1_oclock',
        7  : 'yellow',
        8  : 'red'
    }    
    
    # This maps output channels to motors. There are 3 channels per motor.
    # The first channel is the motor's PWM.
    # The second and third channels are the boolean directions.
    _MOTORS = (8, 9, 10)
    
    def __init__(self, pull_callback=None):
        
        # Buttons (string pull)
        self._pull_callback = pull_callback
        
        # Base audio path
        self._audio_path = ''
        
        # Audio
        self._prompt_queue = []  # Next to play
        self._channel = None  # Currently playing audio
        self._audio_thread = None
        self._current_prompt = None
        
        self._audio_lock = threading.Lock()
        
        # Motors (sing the adafruit motor board)
        self._bus = smbus.SMBus(1)
        self._address = 0x60     
               
        self._bus.write_byte_data(self._address, 0, 1)  # ALLCALL enabled (optional)
        time.sleep(0.005)  # Wait for oscillator
            
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for s in FarmerSays._PIN_NAMES:
            GPIO.setup(s, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            if pull_callback:
                GPIO.add_event_detect(s, GPIO.RISING, callback=self._pull_handler, bouncetime=1000)
                
    def set_audio_path(self, path):
        self._audio_path = path
                
    def start_audio_thread(self):
        self._audio_thread = threading.Thread(target=self._audio_thread_run)
        self._audio_thread.start()      
    
    def is_playing_prompt(self):
        """ Returns true if there is audio playing """       
        ret = False  
        # LOCK
        with self._audio_lock:                   
            if self._channel or self._prompt_queue:
                ret = True        
        # UNLOCK
        return ret
    
    def queue_prompt(self, prompt, path=None):
        """ Add a prompt to the end of the queue """
        if path is None:
            path = self._audio_path
        # [fname,volume,text]
        # LOCK
        with self._audio_lock:
            prompt[0] = path + prompt[0]
            self._prompt_queue.append(prompt)
        # UNLOCK
    
    def get_prompt_queue(self):
        """ Return a copy of the current prompt queue """
        # LOCK
        with self._audio_lock:
            ret = list(self._prompt_queue)
            if self._current_prompt:
                ret = [self._current_prompt] + ret
        # UNLOCK
        return ret
    
    def stop_audio(self):
        """ Stop all audio and clear any queued prompts """
        # LOCK
        with self._audio_lock:       
            self._prompt_queue.clear()
            if self._channel:
                self._channel.stop()
            self._channel = None
            self._current_prompt = None
        # UNLOCK
            
    def set_motor(self, speed):
        """ Set the motor speed
    
        Positive values are clockwise. Negative values are counterclockwise.
        Pass 'None' to release the motor.    
        
        Parameters:
            speed: 0 to 4095 (positive or negative) or None
        """
                    
        if speed == None:
            # Release the motor
            self._set_pwm(FarmerSays._MOTORS[0], 0, 0)
            self._set_bool(FarmerSays._MOTORS[1], False)
            self._set_bool(FarmerSays._MOTORS[2], False)            
        elif speed < 0:            
            # Counterclockwise
            self._set_pwm(FarmerSays._MOTORS[0], 0, -speed)
            self._set_bool(FarmerSays._MOTORS[1], False)
            self._set_bool(FarmerSays._MOTORS[2], True)  
        else:
            # Clockwise
            self._set_pwm(FarmerSays._MOTORS[0], 0, speed)
            self._set_bool(FarmerSays._MOTORS[2], False)
            self._set_bool(FarmerSays._MOTORS[1], True)  
    
    def spin_pointer(self):
        """ Simulate the original spinning """
        self.set_motor(4000)
        time.sleep(2)
        self.set_motor(None)
        
    # privates #
    
    def _pull_handler(self, pin):
        if self._pull_callback:
            self._pull_callback(FarmerSays._PIN_NAMES[pin])
            
    def _audio_thread_run(self):
        do_wait = False
        while True:
            # LOCK
            with self._audio_lock:
                if self._channel:
                    if self._channel.get_busy():
                        # Prompt is playing ... wait a bit.
                        do_wait = True              
                    else:
                        # Prompt is done. Remove it from current-play.
                        self._channel = None
                        self._current_prompt = None                
                else:
                    if self._prompt_queue:
                        # Ready for next prompt
                        self._current_prompt = self._prompt_queue.pop(0)
                        # [fname,volume,text]
                        # print('Playing', self._current_prompt)
                        snd = pygame.mixer.Sound(self._current_prompt[0])
                        snd.set_volume(self._current_prompt[1])
                        self._channel = snd.play()
                        # TODO cache sounds for repeated play                    
                    else:
                        # Nothing to do. Wait a bit.
                        do_wait = True
            # UNLOCK
            if do_wait:
                do_wait = False
                pygame.time.wait(100)
                    
    def _set_pwm(self, channel, on_cnt, off_cnt):    
        # Each channel has 4 registers (a word for ON time and a word for OFF time)
        self._bus.write_byte_data(self._address, 6 + channel * 4, on_cnt & 0xFF)
        self._bus.write_byte_data(self._address, 7 + channel * 4, on_cnt >> 8)
        self._bus.write_byte_data(self._address, 8 + channel * 4, off_cnt & 0xFF)
        self._bus.write_byte_data(self._address, 9 + channel * 4, off_cnt >> 8)
    
    def _set_bool(self, channel, value):
        # Set the output pin to a solid value -- 1 or 0
        if value:
            self._set_pwm(channel, 4096, 0)
        else:
            self._set_pwm(channel, 0, 4096)
    
    
if __name__ == '__main__':

    def pulled(a):
        print('##', a)
        if fs.is_playing_prompt():
            fs.stop_audio()
        else:
            fs.queue_prompt(['duck_1.wav', 0.5, 'QUACK!'])
        
    fs = FarmerSays(pulled)
    fs.start_audio_thread()

time.sleep(30)
