# Import python libs
import os

# Import third party libs
import msgpack

__virtualname__ = 'msgpack'


async def load(hub, conf):
    '''
    Load up the data from the msgpack file
    '''
    if os.path.isfile(conf['file']):
        with open(conf['file'], 'rb') as rfh:
            return msgpack.loads(rfh.read())
    else:
        return {}


async def dump(hub, data, conf):
    '''
    Dump the persistence running data to disk
    '''
    with open(conf['file'], 'wb+') as wfh:
        wfh.write(msgpack.dumps(data))

