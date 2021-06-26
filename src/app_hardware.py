import json

print('Loading hardware ...')
from engine import GameEngine
from farmer_says import FarmerSays
print('... done')


class Application:

    cmd_map = {
        '12_oclock': 'NORTH',
        '1_oclock': 'USERIGHT',
        '2_oclock': 'GETRIGHT',
        '3_oclock': 'EAST',
        '4_oclock': 'DROPRIGHT',
        '5_oclock': 'LOOK',
        '6_oclock': 'SOUTH',
        '7_oclock': 'ACTION',
        '8_oclock': 'DROPLEFT',
        '9_oclock': 'WEST',
        '10_oclock': 'GETLEFT',
        '11_oclock': 'USELEFT'
    }

    GAMES = ['cooks', 'vertiv', 'says']

    def __init__(self):

        self._hardware = FarmerSays(self.command_pull_callback)
        self._game_number = 0

        self.reinit()

        self._hardware.start_audio_thread()

    def reinit(self):
        game = Application.GAMES[self._game_number]
        with open('public/' + game + '/ROOMS.json') as f:
            rooms = json.load(f)

        with open('public/' + game + '/OBJECTS.json') as f:
            objects = json.load(f)

        self._engine = GameEngine(objects, rooms)

        self._hardware.set_audio_path('public/' + game + '/audio/')

    def play_prompts(self, prs):
        # stop any existing audio
        self._hardware.stop_audio()
        for pr in prs:
            self._hardware.queue_prompt([pr, 0.25])

    def command_pull_callback(self, cmd):

        if cmd == 'red':
            self.reinit()
            self.command_pull_callback('5_oclock')
            return

        elif cmd == 'yellow':
            self._game_number += 1
            if self._game_number >= len(Application.GAMES):
                self._game_number = 0
            self._hardware.stop_audio()
            self._hardware.queue_prompt([Application.GAMES[self._game_number] + '.wav', 0.25], path='public/')
            return

        cmd = Application.cmd_map[cmd]
        cmd = self._engine.decode_button_command(cmd)
        prs = self._engine.process_command(cmd)

        if prs:
            aud_prs = self._engine.prompts_only(prs)
            self.play_prompts(aud_prs)


if __name__ == '__main__':

    print('Starting')

    app = Application()

    # Handle the restart (no need to if use_console)
    app.command_pull_callback('5_oclock')
