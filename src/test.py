# At the shell prompt:
# speaker-test -l5 -c2 -t wav

import pygame

def test_audio():
    pygame.mixer.init()
    pygame.mixer.music.load("cow.wav")
    pygame.mixer.music.play()
    
