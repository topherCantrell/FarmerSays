import json
import sys
import textwrap

from engine import GameEngine

COLUMNS = 80


class Application:

    def __init__(self, game, use_audio=True):

        if use_audio:
            print('Loading hardware ...')
            from farmer_says import FarmerSays
            print('... done')
            self._hardware = FarmerSays()
            self._hardware.start_audio_thread()
        else:
            self._hardware = None

        with open('public/' + game + '/ROOMS.json') as f:
            rooms = json.load(f)

        with open('public/' + game + '/OBJECTS.json') as f:
            objects = json.load(f)

        self._engine = GameEngine(objects, rooms)

        if self._hardware:
            self._hardware.set_audio_path('public/' + game + '/audio/')

    def print_long(self, txt):
        paras = txt.split('\n')
        for para in paras:
            print(textwrap.fill(para.strip(), COLUMNS))

    def play_prompts(self, prs):

        if not self._hardware:
            return

        # stop any existing audio
        self._hardware.stop_audio()
        for pr in prs:
            self._hardware.queue_prompt([pr, 0.25])

    def console_loop(self):

        known = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'ACTION', 'LOOK',
                 'GETLEFT', 'GETRIGHT',
                 'DROPLEFT', 'DROPRIGHT',
                 'USELEFT', 'USERIGHT']

        replace = {
            'E': 'EAST',
            'W': 'WEST',
            'N': 'NORTH',
            'S': 'SOUTH'
        }

        first_cmd = True
        while True:
            while True:

                if first_cmd:
                    cmd = 'LOOK'
                    first_cmd = False
                else:
                    cmd = input('> ').upper().replace(' ', '')
                    if cmd in replace:
                        cmd = replace[cmd]
                    if cmd not in known:
                        print('## Unknown command:', cmd)
                        continue
                    cmd = self._engine.decode_button_command(cmd.upper())

                prs = self._engine.process_command(cmd)

                if prs:
                    aud_prs = self._engine.prompts_only(prs)
                    self.play_prompts(aud_prs)
                    prs = self._engine.text_only(prs)
                    self.print_long(prs)


if __name__ == '__main__':

    use_audio = 'audio' in sys.argv

    app = Application(sys.argv[1], use_audio)

    app.console_loop()
