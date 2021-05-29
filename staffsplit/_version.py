#!/usr/bin/env python3
# _version.py
__version__ = '1.0.0'
__app__ = 'staff_split'
__author__ = 'Dominic Thibodeau'
__author_email__ = 'dev@hotkeysoft.net'
__description__ = 'Staff Splitter'
__url__ = 'https://github.com/hotkeysoft/staffsplit_py'
__year__ = 2021

def print_version_info():
    v = f'{__app__} {__description__} version {__version__}'
    print(v)
    print('-'*len(v))
    print(f'{__year__} {__author__} {__author_email__}')
    print(__url__)
    