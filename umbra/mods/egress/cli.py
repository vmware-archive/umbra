# Import python libs
import pprint


async def run(hub, pipe, data):
    '''
    Print the egress data pipe to the cli
    '''
    for comp in data:
        pprint.pprint(comp)
    print(len(data))