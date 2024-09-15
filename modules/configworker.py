import configparser

from modules.log import log

configlib = configparser.ConfigParser()


def cfgread():
    log.debug('Initializing Config', module='_cfgread_')
    configlib.read('config.k3')
    config = {
        # Main section
        'proxy_file': configlib.get('Main', 'proxy_file'),
        'url': configlib.get('Main', 'url'),
        'threads': configlib.get('Main', 'threads'),
        # Proxy section
        'bruteforce_type': configlib.getboolean('Proxy', 'bruteforce_type'),
        'proxy_type': configlib.get('Proxy', 'proxy_type'),
        'response_timeout': configlib.get('Proxy', 'response_timeout'),
        # Log section
        'print_invalid': configlib.get('Log', 'print_invalid')}
    return config


def checksettings(config):
    for key, value in config.items():
        if isinstance(value, str) and not value:
            config[key] = log.input(f"Please enter a value for {key}: ")
    return config
