async def run(hub, flows):
    '''
    Execute the models defined in the given flow
    '''
    for pipe in flows:
        hub.tools.loop.ensure_future('models.init.flow', pipe, flows[pipe])


async def flow(hub, pipe, config):
    '''
    Given the config, fire up the model pulling in the data from the respective
    data pipe
    '''
    mod = config['model']
    while True:
        data = await hub.UP[pipe]['model'].get()
        train = []
        if hub.P[pipe]['first']:
            train = hub.P[pipe]['data']
            hub.P[pipe]['first'] = False
        if config.get('train_for'):
            tnum = config['train_for']
            left = tnum - len(hub.P[pipe]['data']) - len(train)
            if left > 0:
                # Move the numberd items from data into train
                # TODO: We can do this better using more math and slices
                while left > 0:
                    if data:
                        train.append(data.pop(0))
                        left -= 1
                    else:
                        break
        # TODO: This is a memory leak. We need to store this seperately and not keep it all in ram
        hub.P[pipe]['data'].extend(data)
        preds = await hub.tools.ref.last(f'models.{mod}.run')(pipe, data, train)
        await hub.persist.init.dump()
        await hub.UP[pipe]['egress'].put({'data': data, 'preds': preds})