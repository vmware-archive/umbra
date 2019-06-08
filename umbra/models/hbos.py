'''
Take dataset X and run it through the knn algorithm
'''

# Import third party libs
from pyod.models.hbos import HBOS

__virtualname__ = 'hbos'


def __mod_init__(hub):
    hub.models.hbos.COMPS = {}


def make_mlo(hub, data, train):
    '''
    Create the Machine Learning Object used for this sequence
    '''
    return HBOS(contamination=0.001)


async def run(hub, pipe, data, train):
    '''
    Run the hbos algorithm on the given dataset
    '''
    if pipe not in hub.models.hbos.COMPS:
        hub.models.hbos.COMPS[pipe] = {'mlo': hub.models.hbos.make_mlo(data, train)}
    mlo = hub.models.hbos.COMPS[pipe]['mlo']
    if train:
        mlo.fit(train)
    if data:
        mlo.fit(data)
        return mlo.predict(data)
    return []