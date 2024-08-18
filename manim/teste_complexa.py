#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 20:15:27 2024

@author: internet, got from chatGPT
"""

from manim import *

class ComplexFunctionAnimation(Scene):
    def construct(self):
        # Create a complex plane
        complex_plane = ComplexPlane(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 2,
            }
        )
        complex_plane.add_coordinates()
        self.add(complex_plane)

        # Define the complex function
        def complex_path(t):
            return np.exp(1j * 2 * np.pi * t)  # Example: unit circle

        # Create a point
        point = Dot().move_to(complex_plane.n2p(complex_path(0)))
        self.add(point)

        # Define the update function for the point
        def update_point(mob, dt):
            update_point.t += dt
            mob.move_to(complex_plane.n2p(complex_path(update_point.t)))

        update_point.t = 0
        point.add_updater(update_point)

        # Animate the point along the path
        self.play(Create(point), run_time=4, rate_func=linear)
        self.wait()

if __name__ == "__main__":
    scene = ComplexFunctionAnimation()
    scene.render()
