async def run(hub, flows):
    '''
    Execute the models defined in the given flow
    '''
    hub.models.TRAIN = {}
    for pipe in flows:
        hub.models.TRAIN[pipe] = 0
        hub.tools.loop.ensure_future('models.init.flow', pipe, flows[pipe])


async def flow(hub, pipe, config):
    '''
    Given the config, fire up the model pulling in the data from the respective
    data pipe
    '''
    mod = config['model']
    print(f'Starting model: {mod}')
    data = []
    train = []
    while True:
        data.extend(await hub.UP[pipe]['model'].get())
        if hub.P[pipe]['first']:
            train.extend(hub.P[pipe]['data'])
            hub.P[pipe]['first'] = False
        if config.get('train_for'):
            tnum = config['train_for']
            left = tnum - hub.models.TRAIN[pipe] - len(train)
            if left > 0:
                # Move the numberd items from data into train
                # TODO: We can do this better using more math and slices
                while left > 0:
                    if data:
                        train.append(data.pop(0))
                        left -= 1
                    else:
                        break
        if data and len(data) < 10:
            continue
        if train and len(train) < config.get('train_for'):
            if not len(train) % 100:
                print(f'Training data prepared: {len(train)}')
            continue
        hub.models.TRAIN[pipe] += len(train)
        if hub.OPT['umbra']['persist']:
            # TODO: This is a memory leak. We need to store this seperately and not keep it all in ram
            hub.P[pipe]['data'].extend(data)
        preds = await hub.tools.ref.last(f'models.{mod}.run')(pipe, data, train)
        if hub.OPT['umbra']['persist']:
            await hub.persist.init.dump()
        await hub.UP[pipe]['egress'].put({'data': data, 'preds': preds})
        data = []
        train = []