import json, sys, re
from log_parser import LogParser


def get_settings():
    print(sys.argv)
    settings = {}

    return True


def log_parser_plugin():

    print('Start Log-Parser......')
    settings = get_settings()
    if not settings:
        print('Invalid command line flags')
        return 1

    lp = LogParser(settings)
    results = lp.log_process()

    if results.status != 'OK':
        print(results.error)
        return 1
    print(results.message)
    return 0


if __name__ == '__main__':

    log_parser_plugin()



