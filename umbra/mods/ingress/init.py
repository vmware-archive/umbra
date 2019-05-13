# Import python libs
import asyncio


async def run(hub, ingress):
    '''
    Start up the ingress systems
    '''
    for key, conf in ingress.items():
        for pipe in conf:
            if pipe not in hub.umbra.PIPES:
                hub.umbra.PIPES[pipe] = asyncio.Queue()
        hub.tools.loop.ensure_future(hub.tools.ref.last(f'ingress.{key}.run')(conf))
