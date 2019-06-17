'''
Take dataset X and run it through the OPTICS algorithm

Flow config:

    model: optics
    optics:
        n_jobs: -1
'''

# Import third party libs
from sklearn.cluster import OPTICS


def __init__(hub):
    hub.models.optics.COMPS = {}


async def run(hub, config, pipe, data, train):
    '''
    Run the OPTICS algorithm on the given dataset
    '''
    if pipe not in hub.models.optics.COMPS:
        kmconfig = config.get('optics', {})
        mlo = OPTICS(n_jobs=kmconfig.get('n_jobs', -1))
        print('Created OPTICS machine learning object:\n', mlo)
        hub.models.optics.COMPS[pipe] = {'mlo': mlo}

    mlo = hub.models.optics.COMPS[pipe]['mlo']
    if train:
        print(f'Training {len(train)} samples')
        mlo.fit(train)
    if data:
        print(f'Predicting {len(data)} samples')
        return list(mlo.fit_predict(data))
    return []
