async def model(hub, name):
    '''
    Execute a single model using one of the pluggable runtime interfaces
    '''
    runtime = hub.umbra.MODELS[name].get('runtime', 'inline')
    await hub.tools.ref.last(f'runtime.{runtime}.run')(name)
