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
    while True:
        raw_data = await hub.UP[pipe]['egress'].get()
        data = hub.tools.ref.last(f'data.{d_mod}.refine')(pipe, raw_data)
        await hub.tools.ref.last(f'egress.{e_mod}.run')(pipe, data)
