'''
The inline runtime is the default runtime and most simple. This runtime
executes the given model on the local process. This runtime is great
for single models, testing and dedicated use situations in production.
'''

async def run(hub, name):
    '''
    Run the named model. It is assumed at this point that the named model
    resides in the configuration data on the hub.

    Please be advised that no functions deeper that this one should directly
    access the configuration data on the hub. All data should be passed as
    paramaters to deeper functions to ensure that they can opperate in
    issolation.
    '''
    model = hub.umbra.MODELS[name]
    hub.umbra.MOD_STORE[name] = {}
    hub.tools.loop.ensure_future(hub.input.init.gather(name, model))
    hub.tools.loop.ensure_future(hub.data.init.handle(name, model))
    hub.tools.loop.ensure_future(hub.models.init.process(name, model))
    hub.tools.loop.ensure_future(hub.persist.init.save(name, model))
    hub.tools.loop.ensure_future(hub.output.init.spit(name, model))