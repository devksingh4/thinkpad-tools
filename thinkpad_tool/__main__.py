# __main__.py

import sys

from .cmd import commandline_parser

if __name__ == '__main__':
    commandline_parser(sys.argv[1:])
