async def run(hub, flows):
    '''
    Execute the models defined in the given flow
    '''
    hub.models.PIPES = {}
    for pipe in flows:
        hub.models.PIPES[pipe] = {}
        hub.tools.loop.ensure_future(hub.models.init.flow(pipe, flows[pipe]))


async def flow(hub, pipe, config):
    '''
    Given the config, fire up the model pulling in the data from the respective
    data pipe
    '''
    mod = config['model']
    while True:
        data = await hub.umbra.MODELS[pipe].get()
        flags = await hub.tools.ref.last(f'models.{mod}.run')(pipe, data)
        await hub.umbra.EGRESS[pipe].put(flags)