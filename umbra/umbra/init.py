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


def __init__(hub):
    hub.pop.conf.integrate(['umbra'], loader='yaml', cli='umbra', roots=True)
    hub.UP = {}
    hub.P = {}
    hub.umbra.init.load_subs()
    hub.flows.init.load()
    hub.umbra.init.start()


def load_subs(hub):
    hub.pop.sub.add(pypath='umbra.flows')
    hub.pop.sub.add(pypath='umbra.persist')
    hub.pop.sub.add(pypath='umbra.ingress')
    hub.pop.sub.add(pypath='umbra.data')
    hub.pop.sub.add(pypath='umbra.models')
    hub.pop.sub.add(pypath='umbra.egress')


def start(hub):
    '''
    Fire up the async loop and add the first coroutine
    '''
    hub.pop.loop.start(
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
