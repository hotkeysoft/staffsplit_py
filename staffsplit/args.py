#!/usr/bin/env python3
import argparse
import logging
import pkg_resources
log = logging.getLogger(__name__)

def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Splits sheet music image in multiple images containing one staff each.',
        fromfile_prefix_chars='@'
    )

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        '--version',
        help="print version info",
        action="store_true"
    )    

    return parser.parse_args(args)