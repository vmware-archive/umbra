# Import python libs
import asyncio
import types


async def run(hub, name, model):
    '''
    This function is used to set up input gathering until the input interface
    has either been killed or exhausted.
    '''
    hub.umbra.QUE[f'input_{name}'] = asyncio.Queue()
    hub.umbra.EVENTS[f'input_{name}'] = asyncio.Event()
    itype = model['input']['type']
    ret = hub.tools.ref.last('input.{itype}.gather')(name, model)
    if isinstance(ret, types.AsyncGeneratorType):
        async for msg in ret:
            await hub.umbra.QUE[f'input_{name}'].put(msg)
            asyncio.sleep(0)
    elif isinstance(ret, types.GeneratorType):
        for msg in ret:
            await hub.umbra.QUE[f'input_{name}'].put(msg)
            asyncio.sleep(0)
    elif asyncio.iscoroutine(ret):
        msg = await ret
        await hub.umbra.QUE[f'input_{name}'].put(msg)
    else:
        await hub.umbra.QUE[f'input_{name}'].put(ret)
    hub.umbra.EVENTS[f'input_{name}'].set()