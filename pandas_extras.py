#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 22:05:26 2024

@author: luiz
"""
import pandas as pd

def filter_df_by_dict(df, filter_v):
    sub_df = df.loc[(df[list(filter_v)] == pd.Series(filter_v)).all(axis=1)]
    return sub_df
