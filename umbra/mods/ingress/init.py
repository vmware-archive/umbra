# Import python libs
import asyncio
import types


async def run(hub, ingress):
    '''
    Start up the coroutines for each ingress pipe
    '''
    for mod, conf in ingress.items():
        for pipe in conf:
            if pipe not in hub.UP:
                hub.UP[pipe] = {}
                hub.UP[pipe]['in'] = asyncio.Queue()
                hub.UP[pipe]['data'] = asyncio.Queue()
                hub.UP[pipe]['model'] = asyncio.Queue()
                hub.UP[pipe]['egress'] = asyncio.Queue()
        hub.tools.loop.ensure_future('ingress.init.flow', mod, conf)


async def flow(hub, mod, conf):
    ret = hub.tools.ref.last(f'ingress.{mod}.run')(conf)
    if asyncio.iscoroutine(ret):
        ret = await ret
        await hub.ingress.init.que(ret)
    elif isinstance(ret, types.AsyncGeneratorType):
        async for chunk in ret:
            await hub.ingress.init.que(chunk)
    elif isinstance(ret, types.GeneratorType):
        for chunk in ret:
            await hub.ingress.init.que(chunk)
    else:
        await hub.ingress.init.que(ret)


async def que(hub, chunk):
    '''
    Take a single return from the ingress functions
    '''
    pipe = chunk['pipe']
    data = chunk['data']
    await hub.UP[pipe]['data'].put(data)