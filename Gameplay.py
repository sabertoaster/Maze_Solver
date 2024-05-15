# Custom imports
from Algorithms.Algorithms import *
from Algorithms.MazeGeneration import Maze, convert as convert_maze
from GridMapObject import GridMapObject
from GridMap import GridMap
from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS, FPS
#from CURR_PLAYER_PARAMS import CURRENT_LEVEL, CURRENT_PLAY_MODE
# Pre-defined imports
import sys
import pygame
import numpy as np
import cv2
import thorpy as tp
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

        # INSTANTIATE PANELS
        self.init_panel()

        # INSTANTIATE PLAYER
    def fill_grid_map(self):
        for i in range(len(self.maze_toString)):
            for j in range(len(self.maze_toString[0])):
                if self.maze_toString[i][j] == '#':
                    self.player.grid_map.get_map(self.player.current_scene).get_grid()[i][j] = GridMapObject.WALL
        self.player.ratio = (self.maze_size[0] * 2 - 1,self.maze_size[0] * 2 - 1) 
        
        
    def play(self, player):
        self.player = player
        # print(self.player.grid_map.get_map(self.player.current_scene).get_grid())
        
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

    def init_panel(self):
        # INSTANTIATE PANELS
        tp.init(self.screen, tp.theme_classic)

        self.escape_buttons = [tp.Button("Resume"), 
                               tp.Button("Restart"), 
                               tp.Button("Save"), 
                               tp.Button("Auto"), 
                               tp.Button("Menu"), 
                               tp.Button("Quit")]
        
        # [MASK], Use to recognize whether the escape buttons is pressed
        self.associated_values = np.full((6,), 0).tolist()
        
        self.escape_box = tp.TitleBox("My titled box", self.escape_buttons)

        self.escape_box.center_on(self.screen)

        def click_resume():
            self.associated_values[0] = 1

        def click_restart():
            self.associated_values[1] = 1

        def click_save():
            self.associated_values[2] = 1

        def click_auto():
            self.associated_values[3] = 1

        def click_menu():
            self.associated_values[4] = 1

        def click_quit():
            self.associated_values[5] = 1
        
        self.escape_buttons[0].at_unclick = click_resume
        self.escape_buttons[1].at_unclick = click_restart
        self.escape_buttons[2].at_unclick = click_save
        self.escape_buttons[3].at_unclick = click_auto
        self.escape_buttons[4].at_unclick = click_menu
        self.escape_buttons[5].at_unclick = click_quit

        def before_gui(): #add here the things to do each frame before blitting gui elements
            self.screen.fill((250,)*3)

        tp.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

        
        
    def visualize_maze(self):
        pass

    
    def toggle_panel(self, event):
        def at_refresh():
            self.screen.fill((255,)*3)

        self.player.deactivate(active=False)
        m = self.escape_box.get_updater(fps = FPS, esc_quit = True)
        
        while m.playing:
            events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()

            at_refresh()
            m.update(events = events, mouse_rel = mouse_rel)
            pygame.display.flip()

            for event in events:
                if event.type == pygame.QUIT:
                    m.playing = False
                if event.type == pygame.KEYDOWN:
                    key_pressed = event.key

                    if key_pressed == pygame.K_ESCAPE:
                        return "Menu", SCENES["Menu"]["initial_pos"]
                    elif key_pressed == pygame.K_m:
                        m.playing = False
                
                if event.type == pygame.MOUSEBUTTONUP:
                    print(self.associated_values)
                    if self.associated_values[0]: #If click resume button
                        self.associated_values = np.full((6,), 0).tolist()
                        return "Gameplay", self.player.grid_pos
                    if self.associated_values[1]: #If click restart button
                        pass
                    if self.associated_values[2]: #If click save button
                        pass
                    if self.associated_values[3]: #If click auto button
                        pass
                    if self.associated_values[4]: #If click menu button
                        return "Menu", SCENES["Menu"]["initial_pos"]
                    if self.associated_values[5]: #If click quit button
                        sys.exit(0)
                        pygame.exit()

        return "Menu", SCENES["Menu"]["initial_pos"]


# screen = pygame.display.set_mode((1300, 900))
# test = Gameplay(screen, (0,0), (9, 9))
# test.play()