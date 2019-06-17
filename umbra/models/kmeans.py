'''
Take dataset X and run it through the k-means algorithm

Flow config:

    model: kmeans
    kmeans:
        n_clusters: 20
        n_init: 10
        max_iter: 500
'''

# Import third party libs
from sklearn.cluster import KMeans


def __init__(hub):
    hub.models.kmeans.COMPS = {}


async def run(hub, config, pipe, data, train):
    '''
    Run the k-means algorithm on the given dataset
    '''
    if pipe not in hub.models.kmeans.COMPS:
        kmconfig = config.get('kmeans', {})
        mlo = KMeans(n_clusters=kmconfig.get('n_clusters', 8),
                     n_init=kmconfig.get('n_init', 10),
                     max_iter=kmconfig.get('max_iter', 300))
        print('Created k-means machine learning object:\n', mlo)
        hub.models.kmeans.COMPS[pipe] = {'mlo': mlo}

    mlo = hub.models.kmeans.COMPS[pipe]['mlo']
    if train:
        print(f'Training {len(train)} samples')
        mlo.fit(train)
    if data:
        print(f'Predicting {len(data)} samples')
        return list(mlo.predict(data))
    return []
