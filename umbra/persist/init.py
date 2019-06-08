async def load(hub):
    '''
    Look to the configured persistence system and load up the most recent
    dataset into the persist system
    '''
    p_name = hub.OPT['umbra']['persist']
    hub.P = await hub.tools.ref.last(f'persist.{p_name}.load')()
    # We need to set the pipe's flag to let the ingestion know to re-train on historic data
    for pipe in hub.P:
        hub.P[pipe]['first'] = True


async def dump(hub):
    '''
    Take the current data from the runnign pipes and save it
    '''
    p_name = hub.OPT['umbra']['persist']
    await hub.tools.ref.last(f'persist.{p_name}.dump')(hub.P)