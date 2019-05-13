# Import python libs
import asyncio


def new(hub):
    hub.tools.conf.integrate(['umbra'], cli='umbra')
    hub.umbra.PIPES = {}
    hub.umbra.MODELS = {}
    hub.umbra.init.load_subs()


def load_subs(hub):
    hub.tools.sub.add('flows', pypath='umbra.mods.flows')
    hub.tools.sub.add('ingress', pypath='umbra.mods.ingress')
    hub.tools.sub.add('data', pypath='umbra.mods.data')
    hub.tools.sub.add('models', pypath='umbra.mods.models')
    hub.tools.sub.add('persist', pypath='umbra.mods.persist')
    hub.tools.sub.add('egress', pypath='umbra.mods.egress')


def start(hub):
    '''
    Fire up the async loop and add the first coroutine
    '''
    hub.tools.loop.start(
        hub.umbra.init.run(),
        hold=True)


async def run(hub):
    '''
    Start up the flows process
    '''
    hub.umbra.INBOUND = asyncio.Queue()
    hub.tools.loop.ensure_future(hub.ingress.init.run(hub.umbra.INGRESS))
    hub.tools.loop.ensure_future(hub.data.init.run(hub.umbra.FLOWS))
    hub.tools.loop.ensure_future(hub.models.init.run(hub.umbra.FLOWS))