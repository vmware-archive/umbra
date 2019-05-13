# Import python libs
import json


async def run(hub, conf):
    '''
    Read in the configured json files full of juicy data. Add those files' data to the named pipe
    '''
    for pipe in conf:
        for fn in conf[pipe]:
            with open(fn, 'r') as rfh:
                data = json.dumps(rfh.read())
            # TODO: These functions should return and should not need to interact with the pipes
            await hub.umbra.PIPES[pipe].put(data)