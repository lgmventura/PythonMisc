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
índice = 3

zoom_factor = 2.0

format_complex = lambda z: str(round(z.real, 1)) + ("-" if z.imag < 0 else "+") + str(round(z.imag, 1)) + 'i'

class CenaRaizQuadrada(mn.Scene):
    def construct(self):
        tex_lines = mn.VGroup(
            mn.Text(
                "Por que uma só raiz quadrada de um número?",
                #font='Arial',
                font_size=36,
                t2f={'raiz quadrada': 'consolas'},
                t2c={'raiz quadrada': mn.GREEN},
                ),
            mn.MathTex(r'\sqrt{4}'),  # t_comp
            mn.MathTex('{{x}}^2', '=', '4'),
            mn.MathTex('{{x}}', '=', '\pm', '\sqrt', '{4}'),
            mn.MathTex('{{x}}', '=', '\pm', '2'),
            ).arrange(mn.DOWN, buff=0.4)
        
        t_comp = mn.MathTex('= 2')
        t_comp.next_to(tex_lines[1], mn.RIGHT)
        
        self.play(mn.Write(tex_lines[0]))
        self.wait()
        self.play(mn.Write(tex_lines[1]))
        self.wait()
        self.play(mn.Write(t_comp))
        self.wait()
        self.play(mn.Write(tex_lines[2]))
        self.wait()
        self.play(mn.TransformMatchingTex(tex_lines[2].copy(), tex_lines[3],
                                          key_map={'x^2': '\pm', 'x^2': '\sqrt{4}'}))
        self.wait()
        self.play(mn.TransformMatchingTex(tex_lines[3].copy(), tex_lines[4],
                                          key_map={'\sqrt{4}': '2'}))
        self.wait(4)
        self.play(mn.Indicate(tex_lines[3][3]))
        self.wait(8)
        self.play(mn.Indicate(tex_lines[3][2]))
        self.wait()

class cenaRaizCúbica(mn.Scene):
    def construct(self):
        tex_lines = mn.VGroup(
            mn.Paragraph(
                #"Se adotássemos uma convenção na qual o síbolo √\nresultasse em ±, o que aconteceria com",
                "Agora, vamos pensar na raiz cúbica",
                #font='Arial',
                font_size=36,
                ),
            mn.MathTex('\sqrt[3]{n}'), #, '?'),
            mn.MathTex('\sqrt[3]{8}', '=', '2'),
            mn.Text("Analogamente, vamos tomar a equação cúbica:", font_size=24),
            mn.MathTex('{{{x}}}^3', '=', '8')
            ).arrange(mn.DOWN, buff=0.2)
        self.play(mn.Write(tex_lines[0], run_time=1))
        self.wait()
        self.play(mn.Write(tex_lines[1]))
        self.wait(4)
        self.play(mn.Write(tex_lines[2]))
        self.wait(2)
        self.play(mn.Write(tex_lines[3]))
        self.wait()
        self.play(mn.Write(tex_lines[4]))
        self.wait()
    

class CenaSoluçãoEq(mn.Scene):
    def construct(self):
        
        # t = mn.MathTex(r'\sqrt['  + str(índice) + r']{' + str(radicando) + '}')
        tex_lines = mn.VGroup(
            mn.MathTex(f'{{x}}^',f'{índice}', '=', f'{radicando}'),
            mn.Tex('Equações deste tipo, ','${x}$','$^{m}$ ','$ = $',' ${n}$',', nas quais ','${n}$',' é uma constante, possuem, no máximo, 2 raízes reais.'),
            mn.Tex('Portanto, para qualquer ','${m}$','$ > 2$, teremos raízes complexas.'),
            ).arrange(mn.DOWN, buff=0.4).set_width(mn.config.frame_width - 1)
        
        
        # Define a color map for multiple substrings
        color_map = {
            "{x}": mn.GREEN,
            "{m}": mn.BLUE_C,
            f"{índice}": mn.BLUE_C,
            "{n}": mn.ORANGE,
            f"{radicando}": mn.ORANGE
        }
        
        tex_lines[0].set_color_by_tex_to_color_map(color_map)
        tex_lines[1].set_color_by_tex_to_color_map(color_map)
        tex_lines[2].set_color_by_tex_to_color_map(color_map)
        
        self.play(mn.Write(tex_lines[0], run_time=1))
        self.wait()
        self.play(mn.Write(tex_lines[1], run_time=4))
        self.wait()
        self.play(mn.Write(tex_lines[2], run_time=2))
        self.wait(5)
        # self.clear()
        
class CenaSoluçãoEq2(mn.Scene):
    def construct(self):
        width = mn.config.frame_width/2 * 0.9
        # eq_r_str = ''.join('$r = \sqrt[', f'{índice}', ']{', f'{radicando}', '}', ' = ', f'{np.power(radicando, 1/índice)}$')
        tex_lines = mn.VGroup(
            mn.Tex('Vamos considerar ','$i = \sqrt{-1}$',' e lembrar que podemos representar um número complexo qualquer na forma retangular, ','$a + bi$',',  e polar, ','$re^{i\phi}$','.',
                   ),
            # mn.Math
            
            
            # will come after
            mn.Tex('Reescrevendo a equação com a constante ', '$n$', ' na forma polar:'),
            mn.MathTex('x', f'^{índice}', ' = ', f'{radicando}', r'e^{','{i}','2k\pi}'),#, '\longrightarrow', 'x', '=', '\sqrt[índice]{}'),
            mn.MathTex('{x}', '=', f'\sqrt[{índice}]' + '{' + f'{radicando}', 'e^{','{i}','2k\pi}}'),
            mn.MathTex('{x}', '=', f'\sqrt[{índice}]' + f'{{{radicando}}}', 'e^{','{i}', r'\frac{2k\pi}{', f'{índice}' + '}'),
            mn.Tex('Daí, temos o raio ', f'$r = \sqrt[{índice}]{{{radicando}}}$', '$ = $', f'${np.power(radicando, 1/índice):.4g}$'.replace('.', ',')),
            mn.Tex('E os ângulos ', f'${índice}$', '$\\theta$', '$ = $', '$2k\pi$'),
            mn.MathTex('\\theta', ' = ', r'\frac{2k\pi}' + f'{{{índice}}}', ';',),
            
            
            ).arrange(mn.DOWN, buff=0.4).set_width(width)
        
        k_text = mn.MathTex('k = ', f"{'; '.join(str(k) for k in list(range(índice)))}", font_size=12)
        
        
        color_map = {'$i = \sqrt{-1}$': mn.GREEN,
                     '{n}': mn.BLUE_C,
                     f'{índice}': mn.BLUE_C,
                     '{i}': mn.GREEN,
                     '$a + bi$': mn.RED,
                     '$re^{i\phi}$': mn.YELLOW,
                     '{a}': mn.ORANGE,
                     '2k\pi': mn.PURPLE,
                     }
        
        tex_lines[0].set_color_by_tex_to_color_map(color_map)
        tex_lines[1].set_color_by_tex_to_color_map(color_map)
        tex_lines[2].set_color_by_tex_to_color_map(color_map)
        # tex_lines[5].set_color_by_tex_to_color_map(color_map)
        tex_lines[6].set_color_by_tex_to_color_map(color_map)
        # tex_lines[7].set_color_by_tex_to_color_map(color_map)
        
        rg = np.round(2*np.power(radicando, 1/índice))
        complex_plane = mn.ComplexPlane(
            x_range=[-rg, rg, 1],
            y_range=[-rg, rg, 1],
            background_line_style={
                "stroke_color": mn.BLUE_D,
                "stroke_width": 2,
            }
        ).add_coordinates()
        
        tex_lines.to_edge(mn.LEFT)#, buff=-1)
        complex_plane.to_edge(mn.RIGHT, buff=-1)
        # complex_plane.shift([width/2, 0, 0])  # dá no mesmo
        # complex_plane.scale(3/rg)
        
        k_text.next_to(tex_lines[7], mn.RIGHT)
        
        point = complex(-1, -2)
        # cvt = mn.ComplexValueTracker(value=complex(1, 2))
        d = mn.Dot(complex_plane.n2p(point), color=mn.BLUE_A)
        
        path = mn.Line(complex_plane.n2p(-1 - 2j), complex_plane.n2p(2 + 1j))

        # Create an arrow from the point to the x-axis
        arrow_to_x = mn.always_redraw(lambda: mn.Arrow(
            start=complex_plane.n2p(d.get_center()[1] + 1 + 0j),  # Same x, y=0
            end=d.get_center(),
            buff=0,
            max_stroke_width_to_length_ratio=1.5,
            max_tip_length_to_length_ratio=0.08,
            color=mn.RED
        ))
        
        # Create an arrow from the point to the y-axis
        arrow_to_y = mn.always_redraw(lambda: mn.Arrow(
            start=complex_plane.n2p(d.get_center()[1]*1j + 0),  # Same x, y=0
            end=d.get_center(),
            buff=0,
            max_stroke_width_to_length_ratio=1.5,
            max_tip_length_to_length_ratio=0.08,
            color=mn.RED
        ))
        
        # Create an arrow from the point to the y-axis
        arrow_to_d = mn.always_redraw(lambda: mn.Arrow(
            start=complex_plane.n2p(0),  # Same x, y=0
            end=d.get_center(),
            buff=0,
            max_stroke_width_to_length_ratio=1.5,
            max_tip_length_to_length_ratio=0.08,
            color=mn.YELLOW
        ))
        
        angle_arc = mn.always_redraw(lambda: mn.Arc(
            start_angle=0,
            angle=np.arctan(d.get_center()[1]/(d.get_center()[0] - complex_plane.get_center()[0])) + np.pi*((np.sign(d.get_center()[0] - complex_plane.get_center()[0]) - 1)/2),#((np.cos(d.get_center()[0] - complex_plane.get_center()[0])) + np.sin(d.get_center()[1])),
            radius=0.5,
            color=mn.YELLOW
        ).shift(complex_plane.n2p(0)))
        
        p_y_label = mn.always_redraw(lambda: mn.MathTex(
            f"b = {(d.get_center()[1]):.2f}i", font_size=20,
            color=mn.RED
        ).next_to(arrow_to_x, mn.RIGHT, buff=+0.06))
        
        p_x_label = mn.always_redraw(lambda: mn.MathTex(
            f"a = {(d.get_center()[0] - complex_plane.get_center()[0]):.2f}", font_size=20,
            color=mn.RED
        ).next_to(arrow_to_y, mn.UP, buff=+0.06))
        
        p_r_label = mn.always_redraw(lambda: mn.MathTex(
            f"r = {np.sqrt((d.get_center()[0] - complex_plane.get_center()[0])**2 + (d.get_center()[1]**2)):.2f}", font_size=20,
            color=mn.YELLOW
        #).next_to(arrow_to_d, mn.LEFT, buff=+0.1))
        ).move_to(arrow_to_d.get_center()).shift([-0.8, 0, 0]))
        
        p_ang_label = mn.always_redraw(lambda: mn.MathTex(
            f"\phi = {np.arctan(d.get_center()[1]/(d.get_center()[0] - complex_plane.get_center()[0])) + np.pi*((np.sign(d.get_center()[0] - complex_plane.get_center()[0]) - 1)/2):.2f} rad", font_size=20,
            color=mn.YELLOW
        ).move_to(angle_arc.get_center()).shift([0.6, -0.01, 0]))#, mn.DOWN, aligned_edge=d.get_center()))#, buff=-0.1))
        
        # def update_point(mob):
        #     mob.move_to(plane.n2p(path_eq(cvt.get_value())))

        # # update_point.t = 0
        # d2.add_updater(update_point)
        
        
        # graph = complex_plane.plot(lambda t: )
        # graph_label = complex_plane.get_graph_label(graph, label="Número complexo \textit{c}")
        
        self.play(mn.Write(tex_lines[0], run_time=5), mn.Create(complex_plane, run_time=5))
        # self.play()
        self.wait()
        self.play(mn.Create(d))
        self.play(mn.Create(arrow_to_x), mn.Create(arrow_to_y))
        self.play(mn.Create(p_x_label), mn.Create(p_y_label))
        self.play(mn.Create(arrow_to_d), mn.Create(angle_arc))
        self.play(mn.Create(p_r_label), mn.Create(p_ang_label))
        self.wait()
        self.play(mn.MoveAlongPath(d, path), run_time=2)#, rate_func=mn.linear)
        self.wait(6)
        
        self.remove(arrow_to_x, arrow_to_y, p_x_label, p_y_label, arrow_to_d, angle_arc, p_r_label, p_ang_label, d)
        
        points = calc_raízes(radicando, índice)
        points_real = []
        roots_arrows = []
        dots = []
        for point in points:
            points_real.append(complex_plane.n2p(point))
            roots_arrows.append(mn.Arrow(
                complex_plane.n2p(0),
                complex_plane.n2p(point),
                max_stroke_width_to_length_ratio=1.6,
                max_tip_length_to_length_ratio=0.05,
                buff=0.05,
                color=mn.YELLOW,
                ))
            dots.append(mn.Dot(complex_plane.n2p(point), color=mn.RED_C))
        polyg = mn.Polygon(*points_real)
        
        self.play(mn.Write(tex_lines[1]))  # Reescrevendo na forma polar
        self.wait(2)
        self.play(mn.Write(tex_lines[2]))  # x^m = n
        self.wait(12)
        self.play(mn.TransformMatchingTex(tex_lines[2].copy(), tex_lines[3]))  # x = sqrt[m](n)
        self.wait(2)
        self.play(mn.TransformMatchingTex(tex_lines[3].copy(), tex_lines[4]))  # x = sqrt[m](n)
        self.wait(3)
        self.play(mn.Write(tex_lines[5]))  # raio
        self.wait(3)
        self.play(mn.Write(tex_lines[6]))  # ângulo
        self.wait(3)
        self.play(mn.Write(tex_lines[7]))  # ângulo continuação
        self.wait()
        self.play(mn.Write(k_text))
        self.wait()
        
        
        âng = mn.Arc(
                start_angle=0,
                angle=2*np.pi/índice,
                radius=0.5,
                color=mn.YELLOW,
                ).shift(complex_plane.n2p(0))
        
        raio = mn.DoubleArrow(
            complex_plane.n2p(0),
            complex_plane.n2p(points[1]),
            buff=0.05,
            max_stroke_width_to_length_ratio=1.4,
            max_tip_length_to_length_ratio=0.05,
            color=mn.YELLOW,
            )
        
        tex_raio_copy = tex_lines[5].copy()
        tex_ang_copy = tex_lines[7].copy()
        self.play(mn.Indicate(tex_lines[5]))  # indicar raio
        self.play(mn.Transform(tex_raio_copy, raio), run_time=2)
        self.wait()
        self.play(mn.Indicate(tex_lines[7]))  # indicar ângulo
        self.play(mn.Transform(tex_ang_copy, âng), run_time=2)
        self.wait(2)
        
        self.remove(tex_raio_copy, tex_ang_copy)
        self.play(*map(mn.Create, roots_arrows))
        self.play(*map(mn.Create, dots))
        self.wait()
        self.play(mn.Create(polyg))
        self.wait(4)
        self.remove(*roots_arrows, polyg)
        self.wait(2)

class CenaRaízes(mn.MovingCameraScene):
    def construct(self): #, radicando, índice):
        plane = mn.ComplexPlane(x_range=(-int(7*zoom_factor), int(7*zoom_factor)),
                                y_range=(-int(4*zoom_factor), int(4*zoom_factor))).add_coordinates()
        
        # self.camera.frame.scale(1/zoom_factor)
        
        # t = mn.MathTex(r'\sqrt['  + str(índice) + r']{' + str(radicando) + '}')
        t = mn.MathTex(f'{{x}}^{índice}', '=', f'{radicando}')
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
            lb = mn.MathTex("{:.2f}".format(point), font_size=26)#.shift(plane.n2p(point * 1.5)) #.next_to(d, mn.UR, 0.1)
            if np.abs(point.imag) < 0.05:
                lb = lb.shift(plane.n2p(point * 1.6 + 0.2j))
            else:
                lb = lb.shift(plane.n2p(point * 1.3))
            ds.append(d)
            lbs.append(lb)
            self.play(mn.Create(d), mn.Create(lb))
        self.wait()
        
        # clear stuff to render multiple multiplication (exponent) of some points
        points_exponent = [points[0], points[1], points[2], points[3]]  # choose which to show here
        fade_out = [
            mn.FadeOut(t),  # was transformed in polygn, but we need to use the original
            mn.FadeOut(*lbs),
            ]
        self.play(mn.AnimationGroup(*fade_out, lag_ratio=0.1))
        
        self.play(*[dot.animate.fade(0.6) for dot in ds])
        
        self.play(self.camera.frame.animate.scale(zoom_factor))
        
        for point_exp in points_exponent:
            cvt = mn.ComplexValueTracker(value=1)
            d2 = mn.Dot(plane.n2p(point_exp), color=mn.YELLOW)#.add_updater(
                #lambda d: d.move_to(plane.n2p(cvt.get_value())))
            
            # p_mov = point_exp
            
            l2 = mn.MathTex()\
                .add_updater(lambda l: l.become(mn.MathTex("({:.2f})^{{{:.2f}}}".format(point_exp, cvt.get_value().real))))\
                .add_updater(lambda l: l.next_to(d2, mn.UR))
                
            self.play(mn.Create(d2), mn.Create(l2))
            self.wait()
            
            path_eq = lambda t: point_exp**t
                
            for ind in range(1, índice):
                # Define the update function for the point
                def update_point(mob):
                    mob.move_to(plane.n2p(path_eq(cvt.get_value())))
        
                # update_point.t = 0
                d2.add_updater(update_point)
                self.play(cvt.animate.set_value(ind + 1), run_time=1, rate_func=mn.linear)
                # self.play(mn.MoveAlongPath(d2, mov_path))
                self.wait(1)
            
            self.remove(l2)
            
        self.wait()
        
        # show exponentiation paths
        for point_exp in points: #points_exponent:
            path_eq = lambda t: point_exp**t
            exp_graph = mn.ParametricFunction(
                lambda t: plane.n2p(path_eq(complex(t, 0))),
                t_range=[1, índice],
                color=mn.GREEN
                )
            self.play(mn.Create(exp_graph))
            self.wait()
                
        self.wait()

class CenaParÍmpar(mn.Scene):
    def construct(self):
        complex_plane = mn.ComplexPlane(
            x_range=[-8, 8, 1],
            y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": mn.BLUE_D,
                "stroke_width": 2,
            }
        )#.add_coordinates()
        
        self.play(mn.Create(complex_plane))
        
        # polígonos
        r = 3
        d1 = mn.Dot(complex_plane.n2p(r))
        d2 = mn.Dot(complex_plane.n2p(-r))
        self.add(d1)
        for m in range(2, 20):  # polígono
            poly = []
            for p in range(m):
                âng = p * 2*np.pi/m
                point = [r * (np.cos(âng)), r * (np.sin(âng)), 0]
                poly.append(point)
            polyg = mn.Polygon(*poly)
            text = mn.Text(f'm = {m}').move_to(complex_plane.n2p(-3 - 3j))
            
            self.add(text)
            self.add(polyg)
            if m%2 == 0:
                self.add(d2)
            else:
                self.remove(d2)
            self.wait(0.5)
            
            self.remove(text)
            self.remove(polyg)
        
        self.remove(d1)
        self.wait(4)

# cp = CenaRaizQuadrada()
# cp.construct()

# cp = CenaRaízes()
# cp.construct()
