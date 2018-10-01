import os
import pygame

pygame.mixer.init()

def _add_to(filename,cache):
    # sheep_prompt_1
    # sheep_1
    i = filename.index('_')
    an = filename[0:i]
    if an in cache:
        p = cache[an]
    else:
        p = {'next_to_play':0,'filenames':[],'sounds':[]}
        cache[an] = p
        
    p['filenames'].append(filename)  
    snd = pygame.mixer.Sound('../audio/'+filename)
    snd.set_volume(0.05)
    p['sounds'].append(snd)  
    
def _get_next(animal, cache):
    '''    
    {
      next_to_play: 0,
      filenames: [...],
      sounds: [...]
    }    
    '''
    
    # Get the current sound
    a = cache[animal] 
    i = a['next_to_play']
    snd = a['sounds'][i]
    
    # Advance the pointer to the next sound in the array
    i += 1
    if i>= len(a['sounds']):
        i = 0
    a['next_to_play'] = i
    
    return snd    

def get_animal_prompt(animal):
    global _prompts
    return _get_next(animal,_prompts)

def get_animal_sound(animal):
    global _sounds
    return _get_next(animal,_sounds)

def play(animal,wait=False):
    sn = get_animal_sound(animal)
    channel = sn.play(0)
    if wait:
        while channel.get_busy():
            pygame.time.wait(100)

def prompt_and_play(animal):
    pr = get_animal_prompt(animal)
    sn = get_animal_sound(animal)
    
    channel = pr.play(0)
    while channel.get_busy():
        pygame.time.wait(100)
    
    channel = sn.play(0)
    while channel.get_busy():
        pygame.time.wait(100)

files = [f for f in os.listdir('../audio') if os.path.isfile('../audio/'+f)]

_prompts = {}
_sounds = {}

for f in files:
    if '_prompt_' in f:
        _add_to(f,_prompts)
    else:
        _add_to(f,_sounds)
      

