'''
Take dataset X and run it through the knn algorithm
'''

# Import third party libs
from pyod.models.knn import KNN

async def run(hub, pipe, data):
    '''
    Run the knn algorith on the given dataset
    '''
    clf = hub.models.PIPES[pipe].get('clf', KNN())
