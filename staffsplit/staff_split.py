#!/usr/bin/env python3

import logging
import os
import sys
from PIL import Image
from .args import parse_args
from ._version import print_version_info

log = logging.getLogger()

class LogFormatter(logging.Formatter):
    def format(self, record):
        if record.levelno == logging.INFO:
            self._style._fmt = "%(message)s"
        else:
            self._style._fmt = "%(levelname)s: %(message)s"
        return super().format(record)

def main(argv):
    args = parse_args(argv[1:])

    if args.version:
        print_version_info()
        return

    # Configure logging
    old_loglevel = log.level
    handler = logging.StreamHandler()
    handler.setFormatter(LogFormatter())
    log.setLevel(args.loglevel)
    log.addHandler(handler)

    try:
        log.warning('Nothing to do')
    finally:
        # Reset log in case we're not running as a standalong app
        log.removeHandler(handler)
        log.setLevel(old_loglevel)

if __name__ == '__main__':
    MIN_PYTHON = (3, 6)
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)
    main(sys.argv)
