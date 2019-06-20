ROOMS = {

    "room1" : {
        'description' : 'You are in the first room.',
        'description_audio' : 'bark.wav',
        'commands' : {
            'south' : 'GOTO room2'
            }
        },
    
    "room2" : {
        'description' : 'You are in the second room.',
        'description_audio' : 'bark.wav',
        'commands' : {
            'north' : 'GOTO room1'
            }
        },    
    
}


def get_input():
    ret = input('command: ')
    return ret

def handle_room(room):
    node = ROOMS[room]
    print(node['description'])
    inp = get_input()
    if inp in node['commands']:
        print('OK')
        com = node['commands'][inp]
        if com.startswith('GOTO '):
            return com[5:]
    else:
        print("I don't understand.")
        return room

cur_room = 'room1'

while True:
    nr = handle_room(cur_room)
    cur_room = nr