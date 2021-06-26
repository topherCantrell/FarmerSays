import random


class DoneException(Exception):
    pass


class GameEngine:

    def __init__(self, objects, rooms):

        self._objects = objects
        self._rooms = rooms
        self._game = {
            'left_hand': None,
            'right_hand': None,
            'current_room': 'default'
        }
        self._restart = True

        self._COMMANDS = {
            # These are engine commands that can be included in scripts
            'generalDescribeRoom': self.general_describe_current_room,
            'generalGet': self.general_get,
            'generalDrop': self.general_drop,
            'say': self.general_say,
            'goto': self.general_goto,
            'move': self.general_move,
            'replace': self.replace,
            'if': self.conditional,
            'do': self.do_command,
            'restart': self.restart_command,
            'sound': self.object_sound,
        }

    def get_state(self):
        ret = {
            'restart': self._restart,
            'game': self._game,
        }
        rooms = {}
        for name, data in self._rooms.items():
            rooms[name] = {'objects': data['objects']}
        ret['rooms'] = rooms
        return ret

    def set_state(self, state):
        if state:
            self._restart = state['restart']
            self._game = state['game']
            for name, data in state['rooms'].items():
                self._rooms[name]['objects'] = data['objects']
        else:
            self._restart = True

    def restart_command(self, _com, _words):
        self._restart = True

    def object_sound(self, com, words):
        if com == 'sound':
            obj = words[2]
        else:
            obj = com[6:].strip()
        obj = self._objects[obj]
        if 'sound' in obj:
            return [[obj['sound']]]        
        
    def do_command(self, com, words):
        if com == 'do':
            if not words:
                words = []
            return self.process_command(' '.join(words), default_only=True)
        com = com.split()[1:]
        for i in range(len(com)):
            if com[i] == '*':
                com[i] = words[i]
        return self.process_command(' '.join(com))

    def at_start(self):
        script = self._rooms['default']['commands']
        for i in range(0, len(script), 2):
            if script[i] == 'AT_START':
                ret = self._run_script(script[i + 1], [])
                return ret

    def _pull_object(self, obj_name):
        if self._game['left_hand'] == obj_name:
            self._game['left_hand'] = None
            return 'left_hand', 0
        if self._game['right_hand'] == obj_name:
            self._game['right_hand'] = None
            return 'right_hand', 0
        for name, room in self._rooms.items():
            if obj_name in room['objects']:
                i = room['objects'].index(obj_name)
                del room['objects'][i]
                return name, i

    def conditional(self, com, words, next_term):
        com = com.split()
        obj_name = com[1]
        dest = com[3]
        if dest == '_here':
            dest = self._game['current_room']
        elif dest == '_':
            dest = 'default'
        passes = False
        if dest == 'left_hand':
            passes = (self._game['left_hand'] == obj_name)
        elif dest == 'right_hand':
            passes = (self._game['right_hand'] == obj_name)
        elif dest == 'in_hand':
            passes = (self._game['left_hand'] == obj_name) or (self._game['right_hand'] == obj_name)
        else:
            passes = (obj_name in self._rooms[dest]['objects'])

        if passes:
            return self._run_script(next_term, words), (next_term[-1] == 'done')
        else:
            return None, False

    def replace(self, com, _words):
        com = com.split()
        obj_before = com[1]
        obj_after = com[3]
        self._pull_object(obj_after)
        room, ind = self._pull_object(obj_before)
        if room == 'left_hand':
            self._game['left_hand'] = obj_after
        elif room == 'right_hand':
            self._game['right_hand'] = obj_after
        else:
            self._rooms[room]['objects'].insert(ind, obj_after)

    def general_move(self, com, _words):
        com = com.split()
        obj_name = com[1]
        dest = com[3]
        if dest == '_here':
            dest = self._game['current_room']
        elif dest == '_':
            dest = 'default'

        # Remove the target object from any room or hand
        if self._game['left_hand'] == obj_name:
            self._game['left_hand'] = None
        elif self._game['right_hand'] == obj_name:
            self._game['right_hand'] = None
        else:
            for room in self._rooms.values():
                if obj_name in room['objects']:
                    i = room['objects'].index(obj_name)
                    del room['objects'][i]
                    break
                
        dest = self._decode_dest(dest)

        if dest == '_left_hand':
            self._game['left_hand'] = obj_name
        elif dest == '_right_hand':
            self._game['right_hand'] = obj_name
        else:
            room = self._rooms[dest]
            room['objects'].append(obj_name)
            
    def _decode_dest(self, dest):
        if dest.startswith('rand('):
            dest = dest[5:-1].strip().split(',')
            dest = random.choice(dest).strip()
        return dest

    def general_get(self, _com, words):
        cur_room = self._rooms[self._game['current_room']]
        i = cur_room['objects'].index(words[2])
        del cur_room['objects'][i]
        self._game[words[1] + '_hand'] = words[2]
        
    def general_drop(self, _com, words):
        cur_room = self._rooms[self._game['current_room']]
        cur_room['objects'].append(words[2])
        self._game[words[1] + '_hand'] = None
        
    def find_message(self, pr_name):
        pr_name = pr_name.strip()
        if pr_name.startswith('<'):
            return pr_name
        cur_room = self._rooms[self._game['current_room']]
        if 'messages' in cur_room and pr_name in cur_room['messages']:
            pr = cur_room['messages'][pr_name]
        else:
            pr = self._rooms['default']['messages'][pr_name]
        return pr

    def general_say(self, com, _words):
        pr_name = com[4:]
        return [[self.find_message(pr_name)]]

    def general_goto(self, com, words):
        dest = com[5:].strip()
        dest = self._decode_dest(dest)
        self._game['current_room'] = dest
        return self.general_describe_current_room(com, words)

    def general_describe_current_room(self, _com, _words):
        cur_room = self._rooms[self._game['current_room']]
        scr = cur_room['description']
        ret = self._run_script(scr, [])

        obj_dsc = []
        for obj in cur_room['objects']:
            obj_data = self._objects[obj]
            if 'hidden' in obj_data and obj_data['hidden']:
                continue
            prs = obj_data['long']
            if isinstance(prs, list):
                obj_dsc += prs
            else:
                obj_dsc.append(prs)
        if obj_dsc:
            ret.append(obj_dsc)

        if self._game['left_hand']:
            ret.append([
                self.find_message('miscLeftHand'),
                self._objects[self._game['left_hand']]['short']
            ])

        if self._game['right_hand']:
            ret.append([
                self.find_message('miscRightHand'),
                self._objects[self._game['right_hand']]['short']
            ])

        return ret

    def decode_button_command(self, button):

        # NORTH, EAST, SOUTH, WEST, ACTION, LOOK
        # GETLEFT, GETRIGHT, USELEFT, USERIGHT, DROPLEFT, DROPRIGHT

        if button.endswith('LEFT'):
            verb = button[:-4]
            hand = 'left_hand'
            hand_word = 'left'
        elif button.endswith('RIGHT'):
            verb = button[:-5]
            hand = 'right_hand'
            hand_word = 'right'
        else:
            return button.lower()

        if verb == 'GET':
            # get  left/right objToGet objInHand ("-" for nothing)
            current_room = self._game['current_room']
            objs = self._rooms[current_room]['objects']
            obj_word = '-'
            # Find the first non-hidden
            for obname in objs:
                data = self._objects[obname]
                if 'hidden' not in data or not data['hidden']:
                    obj_word = obname
                    break
            for o in objs:
                od = self._objects[o]
                if 'hidden' in od and od['hidden']:
                    continue
                if 'stuck' in od and od['stuck']:
                    continue
                obj_word = o
                break
            in_hand = self._game[hand]
            if not in_hand:
                in_hand = '-'
            return 'get ' + hand_word + ' ' + obj_word + ' ' + in_hand

        elif verb == 'USE':
            in_hand = self._game[hand]
            if not in_hand:
                in_hand = '-'
            return 'use ' + hand_word + ' ' + in_hand

        elif verb == 'DROP':
            in_hand = self._game[hand]
            if not in_hand:
                in_hand = '-'
            return 'drop ' + hand_word + ' ' + in_hand

        else:
            return button

    def _find_command(self, commands, cmd):
        words_in = cmd.split()
        pos = 0
        while pos < len(commands):
            words_targ = commands[pos].split()
            script = commands[pos + 1]
            pos += 2
            # Check the match
            fnd = True
            for i in range(len(words_targ)):
                if words_targ[i] == '*':
                    continue
                if words_targ[i] != words_in[i]:
                    fnd = False
                    break
            if fnd:
                return words_targ, words_in, script

        return None, None, None

    def _run_script(self, script, words):

        if not script:
            return []

        if not isinstance(script, list):
            script = [script]

        ret = []
        pos = 0
        while pos < len(script):
            com = script[pos]
            pos += 1

            i = com.find(' ')
            if i >= 0:
                fw = com[:i]
            else:
                fw = com

            if fw == 'done':
                break

            stop_processing = False
            if fw == 'if':
                prs, stop_processing = self.conditional(com, words, script[pos])
                pos += 1
            else:
                prs = self._COMMANDS[fw](com, words)

            if prs:
                if isinstance(prs, str):
                    ret.append(prs)
                else:
                    ret += prs

            if stop_processing:
                break

        return ret

    def process_command(self, cmd, default_only=False):

        if self._restart:
            self._restart = False
            return self.at_start()

        current_room = self._game['current_room']
        current_room_commands = self._rooms[current_room]['commands']        
        default_commands = self._rooms['default']['commands']
        
        if default_only:
            _match, words, script = None, None, None
        else:
            _match, words, script = self._find_command(current_room_commands, cmd)
            
        if script is None:
            _match, words, script = self._find_command(default_commands, cmd)

        return self._run_script(script, words)

    def text_only(self, prs):
        ret = ''
        for paras in prs:
            for para in paras:
                i = para.find('>')
                para = para[i + 2:]
                if para:
                    ps = para.split('\n')
                    for p in ps:
                        ret += p.strip()
                        if ret[-1] != '@':
                            ret = ret + ' '

        ret = ret.strip().replace('@', '\n')
        return ret

    def prompts_only(self, prs):
        ret = []
        for paras in prs:
            for para in paras:
                i = para.find('>')
                para = para[1:i] + '.wav'
                ret.append(para)
        return ret
