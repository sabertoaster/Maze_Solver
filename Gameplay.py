# Custom imports
from Algorithms.Algorithms import *
from Algorithms.MazeGeneration import Maze, convert as convert_maze, convert_energy
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
from Minimap import Minimap
from Save import*
from Player import*
from random import choice

class Gameplay:
    def __init__(self, screen, start_pos, end_pos,file_name = '', maze_size=(10, 10)):
        self.screen = screen
        self.screenCopy = self.screen.copy()
        self.screen.fill((0, 0, 0))  # Black background [PROTOTYPE]
        self.file_name = file_name
        self.maze_size = maze_size
        #CURRENT_LEVEL.value["maze_size"]
        # INSTANTIATE MAZE
        self.init_maze()

        # INSTANTIATE ALGORITHMS
        self.algorithms = TotalAlgorithms(self.maze_toString)

        # INSTANTIATE PANELS
        self.init_panel()

        # INSTANTIATE PLAYER

        self.minimap_grid_size = (10, 10)

    def fill_grid_map(self):
        for i in range(len(self.maze_toString)):
            for j in range(len(self.maze_toString[0])):
                if self.maze_toString[i][j] == '#':
                    self.player.grid_map.get_map(self.player.current_scene).get_grid()[i][j] = GridMapObject.WALL
        self.player.ratio = (self.maze_size[0] * 2 - 1,self.maze_size[0] * 2 - 1) 

    def update_player(self):
        if self.file_name != '':
            data = read_file(self.file_name)
            self.player.name = data['player.name']
            self.player.re_init(self.player.name, "Gameplay")
            print(self.player.name)
            self.player.grid_pos = data['player.grid_pos']
            self.player.visual_pos = data['player.visual_pos']

    def play(self, player):
        self.player = player
        self.player.grid_pos = self.start_pos[::-1]

        # INSTANTIATE BACKGROUND
        self.init_background()
        # self.screen.blit(self.bg_surface,(0,0))
        self.update_player()
        
        # INSTANTIATE MINIMAP
        minimap_display_pos = (0, (RESOLUTION[0] - RESOLUTION[1]) // 2)
        self.minimap = Minimap(self.screen, RESOLUTION, self.maze_toString, self.minimap_grid_size, self.bg_surface.copy(), self.bg_cell_size , minimap_display_pos, self.player)
        self.minimap.update(self.minimap.maze_surface)

        self.screenCopy = self.screen.copy()
        
        # self.minimap.update(self.screenCopy)
        # self.player.update(self.screenCopy)
        
        self.fill_grid_map()

        solution_flag = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.exit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        next_scene, next_pos = self.toggle_panel(event)
                        if next_scene:
                            self.associated_values = np.full((6,), 0).tolist()

                            return next_scene, next_pos
                    if event.key == pygame.K_m:
                        pass
                        # Handle minimap here       
                    if event.key == pygame.K_x:
                        if not solution_flag:
                            solution_flag = True
                        else:
                            solution_flag = False

                            self.show_solution(solution_flag)
                    if event.key == pygame.K_g:
                        save = SaveFile(self.maze_toString, self.player)
                        save.run_save('test1')
                        
                        # Handle minimap here
                    player_response = self.player.handle_event(event.key)

                    # self.screen.blit(self.screenCopy, (0, 0))
                    # newBG = self.bg_surface.copy()blit(self.player)
                    # newBG.blit(self.player) # Custom function
                    # self.minimap.update(newBG)
                    if player_response == "Move":
                        self.minimap.update(self.minimap.maze_surface)
                    # self.player.update(self.screenCopy)

                    # if solution_flag: 
                    #     ceil_rect = pygame.Rect(self.player.grid_pos[0] * self.cell_size, self.player.grid_pos[1] * self.cell_size, self.cell_size, self.cell_size) # [PROTOTYPE]

                    #     pygame.draw.rect(self.visual_maze, (255,255,255), ceil_rect)

                    #     self.show_solution(solution_flag)

                    pygame.display.update()

    def update_maze(self):
        data = read_file(self.file_name)
        if self.file_name == '':
            self.maze = Maze("Wilson", self.maze_size)
            self.maze_toString = convert_maze(self.maze)
        else:
            self.maze_toString = data['maze_toString']
        
    def init_maze(self):
        # INSTANTIATE MAZE
        self.update_maze()
    
        self.grid_map = GridMap("Maze", self.maze_size, (1, 1))

        self.maze_row, self.maze_col = len(self.maze_toString), len(self.maze_toString[0])

        self.cell_size = 10

        self.draw_maze()

        # test = convert_energy(self.maze_toString)
        # for i in range(len(test)):
        #     for j in range(len(test[0])):
        #         print(test[i][j], end='')
        #     print()

    def init_background(self):
        self.bg_cell_size = RESOLUTION[1] // self.minimap_grid_size[1]

        self.bg_surface = pygame.Surface(((self.maze_row + self.minimap_grid_size[0]) * self.bg_cell_size, (self.maze_col + self.minimap_grid_size[1]) * self.bg_cell_size))
        self.bg_surface.fill((255,51,255))

        maze_surface = pygame.Surface((self.maze_row * self.bg_cell_size, self.maze_col * self.bg_cell_size))

        for i in range(self.maze_row):
            for j in range(self.maze_col):
                ceil_rect = pygame.Rect(j * self.bg_cell_size, i * self.bg_cell_size, self.bg_cell_size, self.bg_cell_size) # [PROTOTYPE]

                if self.maze_toString[i][j] == ' ':
                    pygame.draw.rect(maze_surface, (255,255,255), ceil_rect)
                elif self.maze_toString[i][j] == '#':
                    pygame.draw.rect(maze_surface, (0,0,0), ceil_rect)
                elif self.maze_toString[i][j] == 'S':
                    pygame.draw.rect(maze_surface, (255,255,0), ceil_rect)
                elif self.maze_toString[i][j] == 'E':
                    pygame.draw.rect(maze_surface, (255,0,0), ceil_rect)
        
        self.bg_surface.blit(maze_surface, (self.minimap_grid_size[0] // 2 * self.bg_cell_size, self.minimap_grid_size[1] // 2 * self.bg_cell_size))

    def draw_maze(self):
        self.visual_maze_resolution = (self.maze_row * self.cell_size, self.maze_col * self.cell_size)
        self.visual_maze = pygame.Surface(self.visual_maze_resolution)
        self.visual_maze.fill((0, 0, 0))

        for i in range(self.maze_row):
            for j in range(self.maze_col):
                ceil_rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size) # [PROTOTYPE]

                if self.maze_toString[i][j] == ' ':
                    pygame.draw.rect(self.visual_maze, (255,255,255), ceil_rect)
                elif self.maze_toString[i][j] == '#':
                    pygame.draw.rect(self.visual_maze, (0,0,0), ceil_rect)
                elif self.maze_toString[i][j] == 'S':
                    self.start_pos = (i,j)
                    pygame.draw.rect(self.visual_maze, (255,255,0), ceil_rect)
                elif self.maze_toString[i][j] == 'E':
                    self.end_pos = (i,j)
                    pygame.draw.rect(self.visual_maze, (255,0,0), ceil_rect)

        self.screen.blit(self.visual_maze, (RESOLUTION[0] - self.visual_maze_resolution[0], 0))

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
            self.blur = blur_screen(screen = self.minimap.cut_surface)

            self.screen.blit(self.blur, self.minimap.display_pos)

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
                        self.player.deactivate(active = True)

                        self.screen.blit(self.minimap.cut_surface, self.minimap.display_pos)
                        
                        return None, None
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.associated_values[0]: #If click resume button
                        self.associated_values[0] = 0
                        
                        self.player.deactivate(active = True)

                        self.screen.blit(self.minimap.cut_surface, self.minimap.display_pos)

                        return None, None
                    
                    if self.associated_values[1]: #If click restart button
                        pass
                    if self.associated_values[2]: #If click save button
                        pass
                    if self.associated_values[3]: #If click auto button
                        pass
                    
                    if self.associated_values[4]: #If click menu button
                        self.player.deactivate(active = True)

                        return "Menu", SCENES["Menu"]["initial_pos"]
                    
                    if self.associated_values[5]: #If click quit button
                        sys.exit(0)
                        pygame.exit()

        return None, None

    def show_solution(self, flag):
        trace_path, _ = self.algorithms.a_star(self.player.grid_pos[::-1], self.end_pos)

        if flag:
            color = (127,0,255)
        else:
            color = (255, 255, 255)

        for pos in trace_path:
            ceil_rect = pygame.Rect(pos[1] * self.cell_size, pos[0] * self.cell_size, self.cell_size, self.cell_size)

            pygame.draw.rect(self.visual_maze, color, ceil_rect)

        self.screen.blit(self.visual_maze, (RESOLUTION[0] - self.visual_maze_resolution[0], 0))

        pygame.display.update()
             
# screen = pygame.display.set_mode((1300, 900))
# test = Gameplay(screen, (0,0), (9, 9))
# test.play()