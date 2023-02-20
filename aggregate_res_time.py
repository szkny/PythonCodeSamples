#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20th 21:37:45 2023
   @file  : aggregate_res_time.py
   @author: szkny
   @brief :
"""
import numpy as np
import pandas as pd


# create random time
def getTestData(mu, sig, n):
    return np.cumsum(np.random.normal(mu, sig, n))


test_data = getTestData(2, 0.5, 1000)


df = pd.DataFrame()
df.index.name = 'id'
offset_time = pd.to_datetime('2023-02-20T21:30:00.000')
df['create_time'] = offset_time + pd.to_timedelta(test_data, unit='s')
df.to_csv('./data/res_time.csv')


# aggregate time
df = pd.read_csv('./data/res_time.csv', index_col=0)
df["create_time"] = pd.to_datetime(df["create_time"])
df["diff_time"] = df["create_time"].diff()
df["diff_sec"] = df["diff_time"].map(lambda x: x.seconds + x.microseconds/1e6)

print(df.diff_sec.describe())
print()
print(f'95%tile: {df.diff_sec.quantile(0.95):.6f} sec')
