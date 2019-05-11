def new(hub):
    hub.tools.conf.integrate(['umbra'], cli='umbra')
    hub.umbra.MODELS = {}
    hub.umbra.MOD_STORE = {}
    hub.umbra.init.load()
    hub.umbra.init.start()


def load(hub):
    hub.tools.sub.add('runtime', pypath='umbra.mods.runtime')
    hub.tools.sub.add('input', pypath='umbra.mods.input')
    hub.tools.sub.add('data', pypath='umbra.mods.data')
    hub.tools.sub.add('models', pypath='umbra.mods.models')
    hub.tools.sub.add('persist', pypath='umbra.mods.persist')
    hub.tools.sub.add('output', pypath='umbra.mods.output')


def start(hub):
    '''
    Fire up the async loop and add the first coroutine
    '''
    hub.tools.loop.start(
        hub.umbra.init.run_modes(),
        hold=True)


async def run_models(hub):
    '''
    Execute the models defined in the configuration
    '''
    #TODO: Validate that the model input data is complete and accuate (eventually this should be added directly to conf as a feature)
    for name, model in hub.OPT['umbra']['models'].items():
        hub.umbra.MODELS[name] = model
        hub.tools.loop.ensure_future('runtime.init.model', name)