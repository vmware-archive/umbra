'''
Take dataset X and run it through the knn algorithm
'''

# Import third party libs
from pyod.models.auto_encoder import AutoEncoder

__virtualname__ = 'auto_encoder'


def __mod_init__(hub):
    hub.models.auto_encoder.COMPS = {}


def make_mlo(hub, data, train):
    '''
    Create the Machine Learning Object used for this sequence
    '''
    size = 0
    for chunk in data:
        size = len(chunk)
        break
    for chunk in train:
        size = len(chunk)
        break
    hidden_neurons = [size*2, size, size, size*2]
    return AutoEncoder(hidden_neurons=hidden_neurons, contamination=0.001)


async def run(hub, pipe, data, train):
    '''
    Run the auto_encoder algorithm on the given dataset
    '''
    if pipe not in hub.models.auto_encoder.COMPS:
        hub.models.auto_encoder.COMPS[pipe] = {'mlo': hub.models.auto_encoder.make_mlo(data, train)}
    mlo = hub.models.auto_encoder.COMPS[pipe]['mlo']
    if train:
        mlo.fit(train)
    if data:
        mlo.fit(data)
        return mlo.predict(data)
    return []