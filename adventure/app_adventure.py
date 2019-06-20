ROOMS = {

    "room1": {
        'description': 'You are in the first room.',
        'description_audio': 'bark.wav',
        'commands': {
            'south': 'GOTO room2',
            'north': 'PRINT It is way too cold!'
        }
    },

    "room2": {
        'description': 'You are in the second room.',
        'description_audio': 'bark.wav',
        'commands': {
            'north': 'GOTO room1',
            'south': 'PRINT It is way too hot!'
        }
    },

}


def _com_GET(script_words, inp_words, raw_script, raw_input):
    print("GET NOT IMPLEMENTED")


def _com_GET(script_words, inp_words, raw_script, raw_input):
    print("DROP NOT IMPLEMENTED")


def _com_PRINT(script_words, inp_words, raw_script, raw_input):
    print(raw_script[6:])


def _com_GOTO(script_words, inp_words, raw_script, raw_input):
    GAME['current_room'] = script_words[1]


COMMANDS = {
    'GOTO': _com_GOTO,
    'PRINT': _com_PRINT,
    'GET': _com_GET,
    'DROP': _com_DROP,
}

DEFAULT_COMMANDS = ['GET', 'DROP']

GAME = {
    "current_room": 'room1'
}


def get_input():
    ret = input('command: ')
    return ret


def handle_current_room(room):
    node = ROOMS[GAME['current_room']]
    print(node['description'])
    raw_input = get_input()
    inp = raw_input.split(' ')
    inp[0] = inp[0].lower()
    if inp[0] in node['commands']:
        raw_script = node['commands'][inp[0]]
        script_com = raw_script.split(' ')
        COMMANDS[script_com[0]](script_com, inp, raw_script, raw_input)
        return True
    else:
        print("I don't understand.")
        return False


cur_room = 'room1'

while True:
    handle_current_room(cur_room)
