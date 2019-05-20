async def run(hub, pipe, data):
    '''
    Emit events onto the salt event bus that signal umbra predictions
    '''
    for comp in data:
        hub.SALT_EVENT.fire_event(comp, f'umbra/salt/{pipe}')