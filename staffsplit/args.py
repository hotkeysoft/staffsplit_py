#!/usr/bin/env python3
import argparse
import logging
import os
from posixpath import normpath
import pkg_resources
log = logging.getLogger(__name__)


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Splits sheet music image in multiple images containing one staff each.',
        fromfile_prefix_chars='@'
    )

    parser.add_argument(
        'infile',
        help="input image file(s)",
        nargs='*',
    )

    parser.add_argument(
        '--version',
        help="print version info",
        action="store_true"
    )

    debug_group = parser.add_mutually_exclusive_group()
    debug_group.add_argument(
        '--debug',
        help="print debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )
    debug_group.add_argument(
        '-v', '--verbose',
        help="print additional information",
        action="store_const", dest="loglevel", const=logging.INFO,
    )

    return parser.parse_args(args)
