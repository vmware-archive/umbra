CLI_CONFIG = {
    'flows_dir': {
        'options': ['-f'],
        'default': '/etc/umbra/flows',
        'help': 'The location used for storing flow configuration files'
        },
    'config': {
        'options': ['-c'],
        'default': '/etc/umbra/umbra.conf',
        'help': 'The location to store umbra configuration files',
        },
    'persist': {
        'options': ['-p'],
        'default': {'msgpack': {'file': '/var/cache/umbra/data.mp'}},
        'render': 'yaml',
        'help': 'Define the persistence system and options',
        },
    }
CONFIG = {
    'flows_dir': {
        'options': ['-f'],
        'default': '/etc/umbra/flows',
        'help': 'The location used for storing flow configuration files'
        },
    'config': {
        'options': ['-c'],
        'default': '/etc/umbra/umbra.conf',
        'help': 'The location to store umbra configuration files',
        },
    'persist': {
        'options': ['-p'],
        'default': {'json': {'file': '/var/cache/umbra/data.json'}},
        'render': 'yaml',
        'help': 'Define the persistence system and options',
        },
    }
GLOBAL = {}
SUBS = {}
