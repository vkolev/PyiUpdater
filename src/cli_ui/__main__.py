#!/usr/bin/env python

import os
import sys

path = os.path.realpath(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(path)))

import cli_ui

if __name__ == '__main__':
    cli_ui.main()
