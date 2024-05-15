# Custom imports
from Algorithms.Algorithms import *
from Algorithms.MazeGeneration import Maze, convert as convert_maze
from GridMapObject import GridMapObject
from GridMap import GridMap
from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS
#from CURR_PLAYER_PARAMS import CURRENT_LEVEL, CURRENT_PLAY_MODE
# Pre-defined imports
import sys
import pygame
import numpy as np
import cv2
from enum import Enum
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element
from Visualize.TextBox import TextBox, FormManager, Color
from Visualize.MouseEvents import MouseEvents
from Visualize.Transition import Transition
from Visualize.HangingSign import HangingSign

class Gameplay:
    def __init__(self, screen, start_pos, end_pos, maze_size=(10, 10)):
        self.screen = screen
        self.screenCopy = self.screen.copy()
        self.screen.fill((0, 0, 0))  # Black background [PROTOTYPE]

        self.maze_size = maze_size
        #CURRENT_LEVEL.value["maze_size"]
        # INSTANTIATE MAZE
        self.init_maze()

        # INSTANTIATE ALGORITHMS
        self.algorithms = TotalAlgorithms(Maze)

        # INSTANTIATE PLAYER
    def fill_grid_map(self):
        for i in range(len(self.maze_toString)):
            for j in range(len(self.maze_toString[0])):
                if self.maze_toString[i][j] == '#':
                    self.player.grid_map.get_map(self.player.current_scene).get_grid()[i][j] = GridMapObject.WALL
        self.player.ratio = (self.maze_size[0] * 2 - 1,self.maze_size[0] * 2 - 1) 
        
        
    def play(self, player):
        self.player = player
        print(self.player.grid_map.get_map(self.player.current_scene).get_grid())
        
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        
        self.fill_grid_map()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_scene, next_pos = self.toggle_panel(event)
                        if next_scene:
                            return next_scene, next_pos
                    if event.key == pygame.K_m:
                        pass
                        # Handle minimap here
                    player_response = self.player.handle_event(event.key)
                    self.player.update(self.screenCopy)

    def init_maze(self):
        # INSTANTIATE MAZE
        self.maze = Maze("Wilson", self.maze_size)
        self.maze_toString = convert_maze(self.maze)
        print(self.maze_toString)

        self.grid_map = GridMap("Maze", self.maze_size, (1, 1))

        
                
        self.cell_size = 40
        self.visual_maze = self.screen.copy()
        self.visual_maze.fill((0, 0, 0))
        for i in range(len(self.maze_toString)):
            for j in range(len(self.maze_toString[0])):
                ceil_rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size) # [PROTOTYPE]

                if self.maze_toString[i][j] == ' ':
                    pygame.draw.rect(self.visual_maze, (255,255,255), ceil_rect)
                elif self.maze_toString[i][j] == '#':
                    pygame.draw.rect(self.visual_maze, (0,0,0), ceil_rect)
                elif self.maze_toString[i][j] == 'E':
                    pygame.draw.rect(self.visual_maze, (255,255,0), ceil_rect)
                elif self.maze_toString[i][j] == 'S':
                    pygame.draw.rect(self.visual_maze, (255,0,0), ceil_rect)

        self.screen.blit(self.visual_maze, (0, 0))
        
    def visualize_maze(self):
        pass

    def toggle_panel(self, event):
        self.screenCopy.blit(self.screen, (0, 0))
        while True:
            for event in pygame.event.get():
                pass
                # Handle here
            # pygame.display.flip()
            # self.clock.tick(FPS)
            return None, None

# screen = pygame.display.set_mode((1300, 900))
# test = Gameplay(screen, (0,0), (9, 9))
# test.play()