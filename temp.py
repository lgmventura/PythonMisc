#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 22:13:03 2020

@author: luiz
"""
import random
import numpy as np
import matplotlib.pyplot as plt

def sorteio():
    resultado = random.choice(["AA", "Aa", "aA", "aa"])
    if resultado == 'aa' and random.randint(0, 10) >= 7:
        resultado = 'morto'
    return resultado

resultados = np.array([])

for i in range(100):
    res = sorteio()
    resultados = np.append(resultados, res)

def agruparAlelos(alelos):
    for i in range(len(alelos)):
        if alelos[i] == 'aA':
            alelos[i] = 'Aa'

