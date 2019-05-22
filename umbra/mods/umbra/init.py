# Import python libs
import asyncio

# Application data flow:
# Flows saved to hub.umbra.INGRESS and hub.umbra.FLOWS
# Data pipe saved to hub.UP
# hub.UP[pipe][in]
# hub.UP[pipe][data]
# hub.UP[pipe][model]
# hub.UP[pipe][persist]
# hub.UP[pipe][egress]


def new(hub):
    hub.tools.conf.integrate(['umbra'], loader='yaml', cli='umbra', roots=True)
    hub.UP = {}
    hub.P = {}
    hub.umbra.init.load_subs()
    hub.flows.init.load()
    hub.umbra.init.start()


def load_subs(hub):
    hub.tools.sub.add('flows', pypath='umbra.mods.flows')
    hub.tools.sub.add('persist', pypath='umbra.mods.persist')
    hub.tools.sub.add('ingress', pypath='umbra.mods.ingress')
    hub.tools.sub.add('data', pypath='umbra.mods.data')
    hub.tools.sub.add('models', pypath='umbra.mods.models')
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
    if hub.OPT['umbra']['persist']:
        await hub.persist.init.load()
    hub.umbra.INBOUND = asyncio.Queue()
    await hub.ingress.init.run(hub.umbra.INGRESS)
    await hub.data.init.run(hub.umbra.FLOWS)
    await hub.models.init.run(hub.umbra.FLOWS)
    await hub.egress.init.run(hub.umbra.FLOWS)