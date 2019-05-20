# Import python libs
import asyncio
import fnmatch
import json


async def run(hub, conf):
    '''
    Take the available events off the bus, match them, and then place them on the correct pipes
    '''
    proc = await asyncio.create_subprocess_shell(
            'salt-run state.event',
            stdout=asyncio.subprocess.PIPE)
    while True:
        line = await proc.stdout.readline()
        line = line.decode()
        comps = line.split(maxsplit=1)
        if len(comps) < 2:
            continue
        tag = comps[0].strip()
        data = json.loads(comps[1])
        group = {}
        for pipe in conf:
            group[pipe] = []
        for pipe in conf:
            for match in conf[pipe]:
                if fnmatch.fnmatch(tag, match):
                    data = json.loads(comps[1].strip())
                    event = {'tag': tag, 'data': data}
                    group[pipe].append(event)
        for pipe in group:
            yield {'pipe': pipe, 'data': group[pipe]}