#!/usr/bin/env python3

import shutil

assert __name__ == '__main__'

SRC = 'src/'
OUT = 'out/'

try:
    shutil.rmtree(OUT)
except FileNotFoundError:
    pass
shutil.copytree(SRC, OUT)
