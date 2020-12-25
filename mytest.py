import json, sys, configparser, re
from log_parser import LogParser
from ConfigParser import ConfigParser, NoSectionError, NoOptionError

def load_config():
    def_settings = {}
    try:
        print('load 1')
        config = configparser.RawConfigParser()
        config.read('log_parser.conf')
        def_settings['in']              = config.get('LOG_PARSER', 'INPUT_FILE')
        def_settings['out']             = config.get('LOG_PARSER', 'OUTPUT_FILE')
        def_settings['max-client-ips']  = config.get('LOG_PARSER', 'MAX_CLIENT_IPS')
        def_settings['max-path']        = config.get('LOG_PARSER', 'MAX_PATH')

#    except (NoSectionError, NoOptionError):
    except:
        print('Incorrect config file. Use default.')
        def_settings = {'in':'log.txt', 'out':'results.json','max-client-ips':10, 'max-path':10}
#        pass
    
    finally:
        print('load config: ')
        print(def_settings)
        return def_settings


def get_settings(cmd):
    print(cmd)
    if len(cmd)%2 == 0:
        return None

    settings = load_config()

    print(cmd)
    for i in range(1, len(cmd), 2):
        flag = cmd[i]
        print(flag, cmd[i+1])
        if not flag.startswith('-') or flag[1:] not in settings:
            return 'Invalid'
        settings[flag[1:]] = cmd[i+1]
        if flag[1:] in ('max-client-ips', 'max-path'):
            if not cmd[i+1].isdight():
                return None
            value = int(cmd[i+1])
            if value < 1 or value > 10000:
                return None
            settings[flag[1:]] = value
    print('get_settings:')
    print(settings)
    return settings


def log_parser_plugin(cmd):

    print('Start plugin......')
    settings = get_settings(cmd)
    if not settings:
        print('Invalid command line flags')
        return 1

    print('Start log_parser...')
    lp = LogParser(settings)
    results = lp.log_process()

    if results['status'] != 'OK':
        print(results['error'])
        return 1
    print(results['message'])
    return 0


if __name__ == '__main__':

    log_parser_plugin(sys.argv)



