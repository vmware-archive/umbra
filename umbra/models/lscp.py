'''
Take dataset X and run it through the knn algorithm
'''

# Import third party libs
from pyod.models.lscp import LSCP

__virtualname__ = 'lscp'


def __mod_init__(hub):
    hub.models.lscp.COMPS = {}


def make_mlo(hub, data, train):
    '''
    Create the Machine Learning Object used for this sequence
    '''
    return LSCP(contamination=0.001)


async def run(hub, pipe, data, train):
    '''
    Run the lscp algorithm on the given dataset
    '''
    if pipe not in hub.models.lscp.COMPS:
        hub.models.lscp.COMPS[pipe] = {'mlo': hub.models.lscp.make_mlo(data, train)}
    mlo = hub.models.lscp.COMPS[pipe]['mlo']
    if train:
        mlo.fit(train)
    if data:
        mlo.fit(data)
        return mlo.predict(data)
    return []