# Import python libs
import os

# Import third party libs
import msgpack

__virtualname__ = 'msgpack'


async def load(hub):
    '''
    Load up the data from the msgpack file
    '''
    path = os.path.join(hub.OPT['umbra']['cache_dir'], 'data.mp')
    if os.path.isfile(path):
        with open(path, 'rb') as rfh:
            return msgpack.loads(rfh.read())
    else:
        return {}


async def dump(hub, data):
    '''
    Dump the persistence running data to disk
    '''
    path = os.path.join(hub.OPT['umbra']['cache_dir'], 'data.mp')
    with open(path, 'wb+') as wfh:
        wfh.write(msgpack.dumps(data))

