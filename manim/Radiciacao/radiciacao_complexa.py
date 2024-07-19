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

zoom_factor = 2.0

format_complex = lambda z: str(round(z.real, 1)) + ("-" if z.imag < 0 else "+") + str(round(z.imag, 1)) + 'i'

class CenaRaízes(mn.MovingCameraScene):
    def construct(self): #, radicando, índice):
        plane = mn.ComplexPlane(x_range=(-int(7*zoom_factor), int(7*zoom_factor)),
                                y_range=(-int(4*zoom_factor), int(4*zoom_factor))).add_coordinates()
        
        # self.camera.frame.scale(1/zoom_factor)
        
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
        ds = []
        lbs = []
        for point in points:
            d = mn.Dot(plane.n2p(point), color=mn.YELLOW)
            lb = mn.MathTex("{:.2f}".format(point)).next_to(d, mn.UR, 0.1)
            ds.append(d)
            lbs.append(lb)
            self.play(mn.Create(d), mn.Create(lb))
        self.wait()
        
        # clear stuff to render multiple multiplication (exponent) of some points
        points_exponent = [points[0], points[1]]  # choose which to show here
        fade_out = [
            mn.FadeOut(t),  # was transformed in polygn, but we need to use the original
            mn.FadeOut(*lbs),
            ]
        self.play(mn.AnimationGroup(*fade_out, lag_ratio=0.1))
        
        self.play(*[dot.animate.fade(0.8) for dot in ds])
        
        self.play(self.camera.frame.animate.scale(zoom_factor))
        
        for point_exp in points_exponent:
            d2 = mn.Dot(plane.n2p(point_exp), color=mn.YELLOW)
            self.play(mn.Create(d2))
            p_mov = point_exp
            p_movs = [p_mov]
            # l1 = mn.MathTex()\
            #     .add_updater(lambda l: l.become(mn.MathTex(format_complex(d2.get_value()))))\
            #     .add_updater(lambda l: l.next_to(d2, mn.UR))
            # self.play(mn.Create(l1))
            for ind in range(1, índice):
                p_mov = p_mov * point_exp
                p1 = (p_movs[-1].real, p_movs[-1].imag, 0)
                p2 = (p_mov.real, p_mov.imag, 0)
                mov_path = mn.Line(p1, p2)
                p_movs.append(p_mov)
                
                self.play(mn.MoveAlongPath(d2, mov_path))
                self.wait()
                
        self.wait()


cp = CenaRaízes()
cp.construct()
