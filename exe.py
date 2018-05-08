#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)
argv = sys.argv
argc = len(argv)
if argc != 2:
    quit()
command = "./%s" % argv[1]
os.system(command)
