#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 10:37:16 2020

@author: luiz
"""

import random

class caraCoroa:
    def __iter__(self):
        return self
    def __next__(self):
        if random.choice(["go", "stop"]) == "stop":
            raise StopIteration  # signals "the end"
        return 1

numPart = 1

vtot = 0
for partida in range(numPart):
    v = 0
    for lance in caraCoroa():
        v = v + 1;
    
    v = 2**v
    vtot = vtot + v

vmed = vtot/numPart

print(vmed)