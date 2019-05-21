import faker
import random
import json
import pprint
import os

USERS = ['thatch', 'frank', 'bob', 'sud', 'mary']
IDS = ['ragnarok', 'thor', 'odin', 'loki']


def gen_events(dates, cmds):
    ret = []
    for cmd in cmds:
        id_ = random.choice(IDS)
        pid = random.randint(1024, 2**16)
        event = {
                'tag': 'salt/beacon/{}/sh/{}'.format(id_, pid),
                'data': {'_stamp': next(dates)[0].isoformat(), 'cmd': cmd['cmd'], 'user': random.choice(USERS), 'args': cmd['args'], 'id': id_},
                }
        ret.append(event)
    return ret


def mkdata(size=100000):
    fake = faker.Faker()

    dates = fake.time_series('-1000d', precision=1)

    ret = []
    cmds = []
    icmds = []
    with open(os.path.join(os.path.expanduser('~'), '.bash_history'), 'r') as rfp:
        pcmds = rfp.readlines()
    for cmd in pcmds:
        if ';' in cmd:
            icmds.extend(cmd.split(';'))
        elif '||' in cmd:
            icmds.extend(cmd.split('||'))
        elif '&&' in cmd:
            icmds.extend(cmd.split('&&'))
        else:
            icmds.append(cmd)
    for cmd in icmds:
        parts = cmd.split()
        final = {'cmd': parts[0]}
        if len(parts) > 1:
            final['args'] = parts[1:]
        else:
            final['args'] = []
        cmds.append(final)
    while len(ret) < size:
        ret.extend(gen_events(dates, cmds))
    return ret

def save():
    ret = mkdata()
    #pprint.pprint(ret)
    with open('shell.json', 'w+') as wfp:
        wfp.write(json.dumps(ret))


save()
