# Import python libs
import json

__virtualname__ = 'json'


def gather(hub, name, model):
    '''
    Gather the model data from a json file
    '''
    path = model['input']['file']
    with open(path, 'r') as rfp:
        return json.loads(rfp.read())
