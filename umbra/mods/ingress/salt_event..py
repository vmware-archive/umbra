# Import salt libs
import salt.utils.event
# Import python libs
import asyncio
import fnmatch


def __mod_init__(hub):
    opts = {'sock_dir': hub.OPT['umbra'].get('salt_sock_dir'), 'ipc_mode': 'tcp', 'transport': 'tcp'}
    sock_dir = opts['sock_dir']
    hub.SALT_EVENT = salt.utils.event.get_master_event(opts, sock_dir)


async def run(hub, conf):
    '''
    Take the available events off the bus, match them, and then place them on the correct pipes
    '''
    while True:
        group = {}
        for pipe in conf:
            group[pipe] = []
        events = hub.SALT_EVENT.get_event(no_block=True)
        if events is None:
            await asyncio.sleep(1)
            continue
        for event in events:
            for pipe in conf:
                for match in conf[pipe]:
                    if fnmatch.fnmatch(event['tag'], match):
                        group[pipe].append(event)
        for pipe in group:
            yield {'pipe': pipe, 'data': group[pipe]}
        await asyncio.sleep(1)