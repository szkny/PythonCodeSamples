#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
for k, v in os.environ.items():
    print("{key} : {value}".format(key=k, value=v))
