# Custom imports
from Algorithms.Algorithms import *
from Algorithms.MazeGeneration import Maze

# Pre-defined imports
import sys
import pygame
import numpy as np
import cv2
from enum import Enum


class Gameplay:
    def __init__(self, screen, res_cel, path_resources, maze_size: tuple[int, int]):
        self.resolution, self.cell = res_cel
        self.pth_re = path_resources
        self.screen = screen
        self.screen.fill((0, 0, 0))     # Black background

        # INSTANTIATE MAZE
        self.maze = Maze(maze_size)

        # INSTANTIATE ALGORITHMS
        self.algorithms = BFS(self.maze.maze)

        # INSTANTIATE PLAYER
    def play(self):

    def visualize_maze(self):
        pass




