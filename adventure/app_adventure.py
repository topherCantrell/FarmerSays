
def _com_GOTO(script, inp, raw_script, raw_input):
    GAME['current_room'] = script[1]


def _com_check_exit(inp, raw_input):
    # If Al has had the soda ... you win
    # Otherise you are turned around
    pass


def _com_check_junk(inp, raw_input):
    # Find the nickel if it hasn't been discovered yet
    pass


def _com_GET(script, inp, raw_script, raw_input):
    print("GET NOT IMPLEMENTED")


def _com_DROP(script, inp, raw_script, raw_input):
    print("DROP NOT IMPLEMENTED")


OBJECTS = {
    'quarter': {'location': 'hidden'},
    'dime': {'location': 'hidden'},
    'nickel': {'location': 'hidden'},
    'wrench': {'location': 'cubes'},
    'watergun': {'location': 'wenxiao'},
    'k8s': {'location': 'hidden'}
}

ROOMS = {

    'lobby': {
        'description': 'This is the lobby where Al sits.',
        'audio': 'a.wav',
        'commands': {
            'south': 'GOTO lab',
            'west': 'GOTO 2nd_landing',
            'east': 'GOTO 1st_hall',
            'north': _com_check_exit
        }
    },

    'lab': {
        'description': 'The lab. Junk bins. A to dumpster dive.',
        'audio': 'b.wav',
        'commands': {
            'north': 'GOTO lobby',
            'east': 'GOTO break',
            'A': _com_check_junk
        }
    },

    'break': {},
    'vending': {},
    'cubes': {},
    '1st_hall': {},
    'conference': {},

    '2nd_landing': {},
    '2nd_hall_west': {},
    '2nd_hall_east': {},
    'wenxiao': {},

    '3rd_landing': {},
    'engineering': {},
    'devops': {}

}


SCRIPT_COMMANDS = {  # Map script text commands to real functions
    'GOTO': _com_GOTO
}

DEFAULT_COMMANDS = {  # These are always available
    'GET': _com_GET,
    'DROP': _com_DROP,
}

GAME = {
    "current_room": 'lobby'
}


def get_input():
    ret = input('command: ')
    return ret


def handle_current_room():
    node = ROOMS[GAME['current_room']]
    print(node['description'])
    raw_input = get_input()
    inp = raw_input.split(' ')
    inp[0] = inp[0].lower()
    if inp[0] in node['commands']:
        raw_script = node['commands'][inp[0]]
        if callable(raw_script):
            raw_script(inp, raw_input)
        else:
            script_com = raw_script.split(' ')
            script_com[0] = script_com[0].upper()
            SCRIPT_COMMANDS[script_com[0]](script_com, inp, raw_script, raw_input)
        return True
    else:
        print("I don't understand.")
        return False


while True:
    handle_current_room()
