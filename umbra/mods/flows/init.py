# Import python libs
import os
# Import third party libs
import yaml

'''
# Flows file format
shell:
    ingress:
        salt_event: 'salt/sh*'
    data: salt_event
    model: knn
    egress: salt_event

net:
    ingress:
        salt_event: 'salt/sh*'
    data: salt_event
    model: k_means
    egress: salt_event
'''


def load(hub):
    '''
    Read in the files that reside in the flows direrctory and merge them into
    the flow map used to run the entire process
    '''
    flows = {}
    f_dir = hub.OPT['umbra']['flows_dir']
    for fn in os.listdir(f_dir):
        full  = os.path.join(f_dir, fn)
        with open(full, 'r') as rfh:
            data = yaml.safe_load(rfh.read())
            flows[full] = data
    hub.umbra.INGRESS, hub.umbra.FLOWS = hub.flows.init.merge(flows)


def merge(hub, flows):
    '''
    Given the flows, find the areas where they converge and merge the related
    ingress data
    '''
    ingress = {}
    r_flows = {}
    for full, data in flows.items():
        for pipe in data:
            if not data[pipe].get('enabled', True):
                continue
            for key in data[pipe]['ingress']:
                if key not in ingress:
                    ingress[key] = {}
                if pipe not in ingress[key]:
                    ingress[key][pipe] = []
                val = data[pipe]['ingress'][key]
                if not isinstance(val, list):
                    ingress[key][pipe].append(val)
                else:
                    ingress[key][pipe].extend(val)
                r_flows[pipe] = data[pipe]
    return ingress, r_flows