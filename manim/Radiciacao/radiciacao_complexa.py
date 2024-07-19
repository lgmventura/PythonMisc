#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon 19 Jun 2023 19:18:56 GMT+2

@author: luiz
"""

import manim as mn
import numpy as np

def calc_raízes(radicando: complex, índice=2):
    raízes = []
    r = np.abs(radicando)
    theta = np.angle(radicando)
    raiz = np.power(r, índice**-1)
    for k in range(índice):
        tk = raiz*(np.cos((theta + 2*np.pi*k)/índice) + 1j*np.sin((theta + 2*np.pi*k)/índice))
        raízes.append(tk)
        
    return raízes

radicando = 8
índice = 5

class CenaRaízes(mn.Scene):
    def construct(self): #, radicando, índice):
        plane = mn.ComplexPlane().add_coordinates()
        
        t = mn.MathTex(r'\sqrt['  + str(índice) + r']{' + str(radicando) + '}')
        points = calc_raízes(radicando, índice)
        self.play(mn.Create(t))
        self.wait()
        self.play(mn.Create(plane))
        self.add(plane)

        points_real = []
        for point in points:
            points_real.append([point.real, point.imag, 0])
        polyg = mn.Polygon(*points_real)
        
        self.play(mn.Transform(t, polyg))
        for point in points:
            d = mn.Dot(plane.n2p(point), color=mn.YELLOW)
            lb = mn.MathTex("{:.2f}".format(point)).next_to(d, mn.UR, 0.1)
            self.play(mn.Create(d), mn.Create(lb))
        self.wait()


cp = CenaRaízes()
cp.construct()
