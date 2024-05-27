#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21st 15:57:35 2024
   @file  : tqdm_sample.py
   @author: szkny
   @brief : tqdm sample code
"""

from tqdm import tqdm
import time

for i in tqdm(range(20)):
    time.sleep(0.1)

bar = tqdm(total=30)
for i in range(bar.total):
    bar.update(1)
    time.sleep(0.1)
bar.close()
