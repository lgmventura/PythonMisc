#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 13:00:20 2024

@author: luiz
"""

from manim import *

class MathTransform(Scene):
    def construct(self):
        # Create the MathTex objects
        eq1 = MathTex("x^2", "=", "4")
        eq2 = MathTex("x", "=", r"\pm", r"\sqrt{4}")

        # Position eq2 below eq1 for clarity before the transformation
        eq2.next_to(eq1, DOWN, buff=1)

        # Display the first equation
        self.play(Write(eq1))
        self.wait(1)

        # Perform the transformation
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(2)

if __name__ == "__main__":
    scene = MathTransform()
    scene.render()