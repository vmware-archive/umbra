async def run(hub, flows):
    '''
    Take the egress data flow, re-normalize the data and then push predictions out
    '''
    for pipe in flows:
        hub.tools.loop.ensure_future('egress.init.flow', pipe, flows[pipe])


async def flow(hub, pipe, conf):
    '''
    Take the given pipe and flow and execute it
    '''
    e_mod = conf['egress']
    d_mod = conf['data']
    if not isinstance(e_mod, list):
        e_mod = [e_mod]
    while True:
        w_preds = await hub.UP[pipe]['egress'].get()
        data = await hub.tools.ref.last(f'data.{d_mod}.refine')(
            pipe,
            w_preds['data'],
            w_preds['preds'])
        for mod in e_mod:
            await hub.tools.ref.last(f'egress.{mod}.run')(pipe, data)
