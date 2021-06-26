
NOT_PROMPTS = ['do ', 'east', 'west', 'north', 'south', 'done', 'goto ', 'if ', 'replace ', 'use ', 'action', 'get ', 'drop ',
               'look', 'generalDescribeRoom', 'generalGet', 'generalDrop', 'AT_START', 'AFTER_EVERY', 'move ', 'restart']


def _process(prs, ret):      
    if isinstance(prs, str):
        prs = [prs]
    
    for pr in prs:
        if isinstance(pr, list):
            _process(pr, ret)
            continue
        if pr == '':
            continue
        ignore = False
        for NP in NOT_PROMPTS:
            if pr.startswith(NP):
                ignore = True
                break
        if ignore:
            continue
        pr = pr.split('\n')
        txt = ''
        for p in pr:
            txt = txt + p.strip() + ' '
        txt = txt.strip()
        if txt.startswith('say '):
            txt = txt[4:]
        ret.append(txt)

    
def find_all_prompts(engine):
    
    ret = []
    
    for room in engine._rooms.values():
                
        if 'description' in room:            
            _process(room['description'], ret)
            
        if 'commands' in room:            
            _process(room['commands'], ret)
            
        if 'messages' in room:
            for m in room['messages'].values():
                _process(m, ret)            
            
    for obj in engine._objects.values():
        if 'short' in obj:
            _process(obj['short'], ret)
            
        if 'long' in obj:
            _process(obj['long'], ret)
        
    prompts = {}    
    for pr in ret:
        if pr.startswith('<'):
            j = pr.index('>')
            name = pr[1:j]
            text = pr[j + 1:].strip()
            if name in prompts:
                raise Exception('duplicate prompt <' + name + '>')
            prompts[name] = text
            
    for pr in ret:
        if pr.startswith('<'):
            continue
        if not pr in prompts:
            raise Exception('undefined prompt <' + pr + '>')
        
    return prompts
