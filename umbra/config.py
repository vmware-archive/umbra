# Things to be aware of:
# 1. The absolute paths get normalized when a non-root user is logged in,
#    so don't complain about it!'
CLI_CONFIG = {
    'flows_dir': {
        'options': ['-f'],
        'default': '/etc/umbra/flows',
        'help': 'The location used for storing flow configuration files'
        },
    'cache_dir': {
        'default': '/var/cache/umbra',
        'help': 'The location for cache files',
        },
    'config': {
        'options': ['-c'],
        'default': '/etc/umbra/umbra.conf',
        'help': 'The location to store umbra configuration files',
        },
    'persist': {
        'options': ['-p'],
        'default': '',
        'help': 'Define the persistence system and options',
        },
    }
CONFIG = {
    'flows_dir': {
        'options': ['-f'],
        'default': '/etc/umbra/flows',
        'help': 'The location used for storing flow configuration files'
        },
    'cache_dir': {
        'default': '/var/cache/umbra',
        'help': 'The location for cache files',
        },
    'config': {
        'options': ['-c'],
        'default': '/etc/umbra/umbra.conf',
        'help': 'The location to store umbra configuration files',
        },
    'persist': {
        'options': ['-p'],
        'default': '',
        'help': 'Define the persistence system and options',
        },
    }
GLOBAL = {}
SUBS = {}
