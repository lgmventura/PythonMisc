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

class ComplexPlane(mn.Scene):
    def construct(self, points):
        plane = mn.ComplexPlane().add_coordinates()
        
        self.play(mn.Create(plane))
        self.add(plane)
        for point in points:
            d = mn.Dot(plane.n2p(point), color=mn.YELLOW)
            lb = mn.MathTex("{:.2f}".format(point)).next_to(d, mn.UR, 0.1)
            # self.add(
            #     d,
            #     lb,
            #     )
            self.play(mn.Create(d))
            self.add(lb)
        self.wait()

points = calc_raízes(8, 3)

cp = ComplexPlane()
cp.construct(points)
