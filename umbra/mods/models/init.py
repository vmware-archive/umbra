async def run(hub, flows):
    '''
    Execute the models defined in the given flow
    '''
    hub.models.PIPES = {}
    for pipe in flows:
        hub.models.PIPES[pipe] = {}
        hub.tools.loop.ensure_future('models.init.flow', pipe, flows[pipe])


async def flow(hub, pipe, config):
    '''
    Given the config, fire up the model pulling in the data from the respective
    data pipe
    '''
    mod = config['model']
    while True:
        data = await hub.UP[pipe]['model'].get()
        preds = await hub.tools.ref.last(f'models.{mod}.run')(pipe, data)
        await hub.UP[pipe]['egress'].put({'data': data, 'preds': preds})