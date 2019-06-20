ROOMS = {

    "room1": {
        'description': 'You are in the first room.',
        'description_audio': 'bark.wav',
        'commands': {
            'south': 'GOTO room2'
        }
    },

    "room2": {
        'description': 'You are in the second room.',
        'description_audio': 'bark.wav',
        'commands': {
            'north': 'GOTO room1'
        }
    },

}

GAME = {
    "current_room": 'room1'
}


def _com_GOTO(script_words, inp_words):
    GAME['current_room'] = script_words[1]


COMMANDS = {
    'GOTO': _com_GOTO
}


def get_input():
    ret = input('command: ')
    return ret


def handle_current_room(room):
    node = ROOMS[GAME['current_room']]
    print(node['description'])
    inp = get_input()
    inp = inp.split(' ')
    inp[0] = inp[0].lower()
    if inp[0] in node['commands']:
        script_com = node['commands'][inp[0]].split(' ')
        COMMANDS[script_com[0]](script_com, inp)
        return True
    else:
        print("I don't understand.")
        return False


cur_room = 'room1'

while True:
    handle_current_room(cur_room)
