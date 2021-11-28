#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  6 23:33:12 2021

@author: luiz
"""
import numpy as np

# original algorithm for searching path

# for arrays of length 3 (cube)
def hex_to_path(start, graph):
    frontier = []
    frontier.append(start)
    came_from = dict()
    came_from[start] = None
    
    while not frontier.empty():
        current = frontier.get()
        for nxt in graph.neighbors(current):
            if nxt not in came_from:
                frontier.put(nxt)
                came_from[nxt] = current
    return came_from

def hex_to_path_dir(start, radius, directions):
    frontier = []
    frontier.append(start)
    came_from = dict()
    start_h = hash(tuple(start))
    came_from[start_h] = None
    
    while not len(frontier) == 0:
        current = frontier.pop(0)
        for d in directions:
            nxt = current + d
            if any([nxt[0] > radius, nxt[1] > radius, nxt[2] > radius]):
                continue
            nxt_h = hash(tuple(nxt))
            if nxt_h not in came_from:
                frontier.append(nxt)
                came_from[nxt_h] = current
    return came_from


# original algorithm for retrieving path

def retrieve_path(came_from, goal):
    current = goal
    
    path = []
    while any(current != start):
       path.append(current)
       current_h = hash(tuple(current))
       current = came_from[current_h]
    path.append(start) # optional
#    path.reverse() # optional
    return path

def path_to_steps(path):
    steps = np.array(path)
    steps = np.diff(steps, axis=0)
    return steps

def steps_to_numSteps(steps, directions):
    ns = np.zeros(len(directions))
    for i, d in enumerate(directions):
        for step in steps:
            if all(d == step):
                ns[i] = ns[i] + 1
    return ns

# tests:
start = np.array([0,0,0]) # anything
goal = np.array([2,2,-4]) # anything

directions = [np.array([3, 0, -3]), np.array([7, -7, 0]), np.array([0, -4, 4]), np.array([-3, 0, 3]), np.array([-7, 7, 0]), np.array([0, 4, -4])]
#directions = [np.array([1, 0, -1]), np.array([1, -1, 0]), np.array([0, -1, 1]), np.array([-1, 0, 1]), np.array([-1, 1, 0]), np.array([0, 1, -1])]

#radius = 128+7+4
radius = 20

came_from = hex_to_path_dir(start, radius, directions)
path = retrieve_path(came_from, goal)
steps = path_to_steps(path)
ns = steps_to_numSteps(steps, directions)

#%%
# 1D version

# for scalar numbers
def create_map(start, radius, directions):
    frontier = []
    frontier.append(start)
    came_from = dict()
    came_from[start] = None
    
    while not len(frontier) == 0:
        current = frontier.pop(0)
        for d in directions:
            nxt = current + d
            if abs(nxt) > radius:
                continue
            if nxt not in came_from:
                frontier.append(nxt)
                came_from[nxt] = current
    return came_from

def retrieve_path1d(came_from, goal):
    current = goal
    
    path = []
    while current != start:
       path.append(current)
       current = came_from[current]
    path.append(start) # optional
#    path.reverse() # optional
    return path

start = 0
goal = 1

directions = [3,-3, 4,-4, 7,-7]

radius = 128

came_from = create_map(start, radius, directions)
path = retrieve_path1d(came_from, goal)
steps = path_to_steps(path)

