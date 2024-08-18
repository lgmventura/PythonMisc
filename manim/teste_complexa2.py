#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 20:40:28 2024

@author: chat gpt
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

        # Create a ValueTracker to control 't'
        t_tracker = ValueTracker(0)

        # Create a point
        point = Dot().move_to(complex_plane.n2p(complex_path(t_tracker.get_value())))
        self.add(point)

        # Define the update function for the point
        def update_point(mob):
            mob.move_to(complex_plane.n2p(complex_path(t_tracker.get_value())))

        point.add_updater(update_point)

        # Animate the ValueTracker
        self.play(t_tracker.animate.set_value(1), run_time=4, rate_func=linear)
        self.wait()

if __name__ == "__main__":
    scene = ComplexFunctionAnimation()
    scene.render()