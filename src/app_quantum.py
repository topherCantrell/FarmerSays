import os
import sys

print('Loading hardware ...')
import farm_adafruit_io
from farmer_says import FarmerSays
print('... done')


class Application:

    cmd_map = {
        '12_oclock': 'Sheep',
        '1_oclock': 'Dog',
        '2_oclock': 'Duck',
        '3_oclock': 'Frog',
        '4_oclock': 'Horse',
        '5_oclock': 'Coyote',
        '6_oclock': 'Rooster',
        '7_oclock': 'Pig',
        '8_oclock': 'Cow',
        '9_oclock': 'Bird',
        '10_oclock': 'Cat',
        '11_oclock': 'Turkey'
    }

    def __init__(self, solo=False, original=False, nospin=False):
        self._solo = solo
        self._original = original
        self._nospin = nospin
        self._hardware = FarmerSays(self._callback_string_pulled)
        self._hardware.start_audio_thread()

        if original:
            audio_dir = '../originalAudio/'
        else:
            audio_dir = '../audio/'

        self._hardware.set_audio_path(audio_dir)

        files = [f for f in os.listdir(audio_dir) if os.path.isfile(audio_dir + f)]
        self._prompts = {}
        self._sounds = {}

        for f in files:
            if '_prompt' in f:
                dest = self._prompts
            else:
                dest = self._sounds
            i = f.find('_')
            if i < 0:
                i = f.find('.')
            an = f[0:i].lower()
            if an in dest:
                p = dest[an]
            else:
                p = {'next_to_play': 0, 'filenames': []}
                dest[an] = p

            p['filenames'].append(f)

    def play_prompt_sound(self, animal):
        prompt = self.get_next(animal, False)
        sound = self.get_next(animal, True)

        if prompt and sound:
            self._hardware.stop_audio()
            self._hardware.queue_prompt([prompt, 0.25])
            self._hardware.queue_prompt([sound, 0.25])
            if not self._nospin:
                self._hardware.spin_pointer()

    def get_next(self, animal, is_sound=True):
        '''
        {
          next_to_play: 0,
          filenames: [...]
        }
        '''

        if is_sound:
            cache = self._sounds
        else:
            cache = self._prompts

        animal = animal.lower()  # The audio files are all lower

        if animal not in cache:
            return None

        # Get the current sound
        a = cache[animal]
        i = a['next_to_play']

        # Advance the pointer to the next sound in the array
        i += 1
        if i >= len(a['filenames']):
            i = 0
        a['next_to_play'] = i

        return a['filenames'][i]

    def _callback_string_pulled(self, cmd):
        animal = Application.cmd_map[cmd]
        if self._solo:
            self.play_prompt_sound(animal)
        else:
            farm_adafruit_io.post_animal(animal)


def main():

    solo = 'solo' in sys.argv
    original = 'original' in sys.argv
    nospin = 'nospin' in sys.argv

    app = Application(solo, original, nospin)

    if not solo:
        while True:
            an = farm_adafruit_io.wait_for_new_animal()
            app.play_prompt_sound(an)


if __name__ == '__main__':
    main()
