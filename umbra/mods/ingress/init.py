# Import python libs
import asyncio


async def run(hub, ingress):
    '''
    Start up the ingress systems
    '''
    for key, conf in ingress.items():
        for pipe in conf:
            if pipe not in hub.UP:
                hub.UP[pipe] = {}
                hub.UP[pipe]['in'] = asyncio.Queue()
                hub.UP[pipe]['data'] = asyncio.Queue()
                hub.UP[pipe]['persist'] = {}
                hub.UP[pipe]['egress'] = asyncio.Queue()
        hub.tools.loop.ensure_future(hub.tools.ref.last(f'ingress.{key}.run')(conf))
