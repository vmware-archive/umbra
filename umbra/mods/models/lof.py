'''
Take dataset X and run it through the knn algorithm
'''

# Import third party libs
from pyod.models.lof import LOF

__virtualname__ = 'lof'


def __mod_init__(hub):
    hub.models.lof.COMPS = {}


def make_mlo(hub, data, train):
    '''
    Create the Machine Learning Object used for this sequence
    '''
    return LOF(contamination=0.001)


async def run(hub, pipe, data, train):
    '''
    Run the hbos algorithm on the given dataset
    '''
    if pipe not in hub.models.lof.COMPS:
        hub.models.lof.COMPS[pipe] = {'mlo': hub.models.lof.make_mlo(data, train)}
    mlo = hub.models.lof.COMPS[pipe]['mlo']
    if train:
        print(f'Training {len(train)} datasets')
        mlo.fit(train)
    if data:
        print(f'Fitting {len(data)} datasets')
        mlo.fit(data)
        print(f'Predicting {len(data)} datasets')
        return mlo.predict(data)
    return []