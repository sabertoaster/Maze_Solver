# Custom imports
from Algorithms.Algorithms import *
from Algorithms.MazeGeneration import Maze, convert as convert_maze, convert_energy
from GridMapObject import GridMapObject
from GridMap import GridMap
from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS, FPS
# from CURR_PLAYER_PARAMS import CURRENT_LEVEL, CURRENT_PLAY_MODE
# Pre-defined imports
import sys
import pygame
import numpy as np
import cv2
import json
import thorpy as tp
from enum import Enum
from Visualize.ImageProcess import blur_screen, morph_image, add_element
from Visualize.TextBox import TextBox, FormManager, Color
from Visualize.MouseEvents import MouseEvents
from Visualize.Transition import Transition
from Visualize.HangingSign import HangingSign
from Minimap import Minimap
from Save import *
from Player import *
from random import choice
import time


class Gameplay:
    def __init__(self, screen, start_pos, end_pos, file_name='', maze_size=(20, 20)):
        self.screen = screen
        self.screenCopy = self.screen.copy()
        self.screen.fill((0, 0, 0))  # Black background [PROTOTYPE]
        self.file_name = file_name
        self.maze_size = maze_size
        # CURRENT_LEVEL.value["maze_size"]

        # INSTANTIATE PANELS
        self.init_panel()

        # INSTANTIATE PLAYER

        self.minimap_grid_size = (20, 20)
        SCENES["Gameplay"]["cell"] = (RESOLUTION[1] // self.minimap_grid_size[0], RESOLUTION[1] // self.minimap_grid_size[0])

    def fill_grid_map(self):
        for i in range(len(self.maze_toString)):
            for j in range(len(self.maze_toString[0])):
                if self.maze_toString[i][j] == '#':
                    self.player.grid_map.get_map(self.player.current_scene).get_grid()[i][j] = GridMapObject.WALL
                else:
                    self.player.grid_map.get_map(self.player.current_scene).get_grid()[i][j] = GridMapObject.FREE
        self.player.ratio = (self.maze_size[0] * 2 - 1, self.maze_size[0] * 2 - 1)

    # def update_player(self):
    #     if self.file_name != '':
    #         data = read_file(self.file_name)
    #         self.player.name = data['player.name']
    #         self.player.re_init(self.player.name, "Gameplay")
    #         print(self.player.name)
    #         self.player.grid_pos = data['player.grid_pos']
    #         self.player.visual_pos = data['player.visual_pos']

    def get_data(self):
        with open("current_profile.json") as fi:
            data = json.load(fi)
            self.player.name = data['player.name']
            self.player.re_init(self.player.name, "Gameplay")
            self.player.grid_pos = data['player.grid_pos']
            self.player.visual_pos = data['player.visual_pos']
            if (data["level"] == "Easy"):
                self.maze_size = (10, 10)
                self.minimap_grid_size = (20, 20)
            elif (data["level"] == "Medium"):
                self.maze_size = (20, 20)
                self.minimap_grid_size = (20, 20)
            elif (data["level"] == "Hard"):
                self.maze_size = (50, 50)
                self.minimap_grid_size = (20, 20)
            SCENES["Gameplay"]["cell"] = (RESOLUTION[1] // self.minimap_grid_size[0], RESOLUTION[1] // self.minimap_grid_size[0])
            if data["maze_toString"]:
                self.maze_toString = data["maze_toString"]

            else:
                self.maze = Maze("Wilson", self.maze_size)
                self.maze_toString = convert_maze(self.maze)

    def play(self, player):
        self.player = player
        self.get_data()

        # INSTANTIATE MAZE
        self.init_maze()

        # INSTANTIATE PLAYER
        self.set_start_pos()
        self.player.grid_pos = self.start_pos[::-1]
        # self.update_player()

        # INSTANTIATE ALGORITHMS
        self.algorithms = TotalAlgorithms(self.maze_toString)

        # INSTANTIATE BACKGROUND
        self.init_background()

        # INSTANTIATE MINIMAP
        minimap_display_pos = (0, 0)
        self.minimap = Minimap(self.screen, self.maze_toString, self.minimap_grid_size, self.bg_surface.copy(),
                               self.bg_cell_size, minimap_display_pos, self.player)
        self.minimap.update(self.minimap.maze_surface)

        self.screenCopy = self.screen.copy()

        # self.minimap.update(self.screenCopy)
        # self.player.update(self.screenCopy)
        self.solution_flag = False

        self.visualize_maze(self.visual_maze, self.solution_flag)
        self.fill_grid_map()
        
        # INSTANTIATE CHOOSE MODE BUTTON
        self.init_choose_mode() # Init buttons
        
        self.choose_mode_flag = True
        choose_mode_launcher = self.choose_mode.get_updater()

        self.manual_flag = False
        manual_launcher = self.hint_button.get_updater()
        self.hint_flag = False
        
        self.auto_index = 0
        self.trace_path, _ = self.algorithms.a_star(self.player.grid_pos[::-1], self.end_pos)
        self.trace_path.insert(0, self.start_pos)
        
        self.auto_flag = False
        auto_launcher = self.auto_button.get_updater()
        
        # Deactivate player to choose mode
        self.player.deactivate(active=False)
        
        while True:
            events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()
            
            if self.choose_mode_flag:
                choose_mode_launcher.update(events = events, mouse_rel = mouse_rel)
            elif self.manual_flag:
                manual_launcher.update(events = events, mouse_rel = mouse_rel)
            elif self.auto_flag:
                self.auto_move()
                
                pygame.time.delay(100)
                
                # Block player keyboard input
                
                auto_launcher.update(events = events, mouse_rel = mouse_rel)
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
                    if event.key == pygame.K_ESCAPE:
                        # Disable spamming button
                        pygame.key.set_repeat()
                        next_scene, next_pos = self.toggle_panel()
                        # Enable spamming button again
                        pygame.key.set_repeat(200, 125)
                        
                        if next_scene:
                            return next_scene, next_pos
                        
                        break
                    if event.key == pygame.K_m:
                        pass
                        # Handle minimap here
                        
                    if event.key == pygame.K_g:
                        save = SaveFile(self.maze_toString, self.player)
                        save.run_save('test1')
                        
                    player_response = self.player.handle_event(event.key)
                    
                    if player_response == "Move" and event.type != pygame.USEREVENT:
                        pygame.event.clear()
                    if self.solution_flag:
                        ceil_rect = pygame.Rect(self.player.grid_pos[0] * self.cell_size, self.player.grid_pos[1] * self.cell_size, self.cell_size, self.cell_size) # [PROTOTYPE]
                        pygame.draw.rect(self.visual_maze, (255,255,255), ceil_rect)
                    
                    self.update_screen()
                    
                pygame.display.update()

    # def update_maze(self):
    #     if self.file_name == '':
    #         self.maze = Maze("Wilson", self.maze_size)
    #         self.maze_toString = convert_maze(self.maze)
    #     else:
    #         data = read_file(self.file_name)
    #         self.maze_toString = data['maze_toString']

    def init_maze(self):
        # INSTANTIATE MAZE
        # self.update_maze()

        self.grid_map = GridMap("Maze", self.maze_size, (1, 1))
        
        self.maze_row, self.maze_col = len(self.maze_toString), len(self.maze_toString[0])
        self.cell_size = (RESOLUTION[0] - RESOLUTION[1]) // min(self.maze_row, self.maze_col)
        
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
                    pygame.draw.rect(self.visual_maze, (170,170,0), ceil_rect)
                elif self.maze_toString[i][j] == 'E':
                    self.end_pos = (i,j)
                    pygame.draw.rect(self.visual_maze, (255,0,0), ceil_rect)

        self.visual_maze_display_pos = (0, RESOLUTION[0] - (RESOLUTION[0] - RESOLUTION[1]) // 2)
        self.screen.blit(self.visual_maze, (RESOLUTION[0] - self.visual_maze_resolution[0], 0))

        # test = convert_energy(self.maze_toString)
        # for i in range(len(test)):
        #     for j in range(len(test[0])):
        #         print(test[i][j], end='')
        #     print()

    def init_background(self):
        self.bg_cell_size = RESOLUTION[1] // self.minimap_grid_size[1]

        screen_size = ((self.maze_row + self.minimap_grid_size[0] + 1) * self.bg_cell_size,
                       (self.maze_col + self.minimap_grid_size[1] + 1) * self.bg_cell_size)


        self.bg_surface = morph_image("Resources/cave_BG.png", screen_size)

        maze_surface = pygame.Surface((self.maze_row * self.bg_cell_size, self.maze_col * self.bg_cell_size),
                                      pygame.SRCALPHA, 32).convert_alpha()

        start = morph_image("Resources/login_box.png", (self.bg_cell_size, self.bg_cell_size))
        end = morph_image("Resources/kitchen_BG.png", (self.bg_cell_size, self.bg_cell_size))
        print(self.bg_cell_size)
        tuan = [
            "cave_wall_1.png",
            "cave_wall_2.png",
            "cave_wall_3.png",
            "cave_wall_4.png",
            "cave_wall_5.png",
            "cave_wall_6.png",
            "cave_wall_7.png",
            "cave_wall_8.png",
        ]
        wall = morph_image(RESOURCE_PATH + "cave_wall.png", (self.bg_cell_size, self.bg_cell_size))
        for i in range(self.maze_row):
            for j in range(self.maze_col):

                pos = (j * self.bg_cell_size, i * self.bg_cell_size)
                if self.maze_toString[i][j] == '#':
                    img = pygame.image.load(RESOURCE_PATH + tuan[np.random.randint(0, len(tuan))]).convert_alpha()
                    maze_surface.blit(img, pos)
                    # pygame.draw.rect(maze_surface, (0,0,0), ceil_rect)
                elif self.maze_toString[i][j] == 'S':
                    maze_surface.blit(start, pos)
                    # pygame.draw.rect(maze_surface, (255,255,0), ceil_rect)
                elif self.maze_toString[i][j] == 'E':
                    maze_surface.blit(end, pos)
                    # pygame.draw.rect(maze_surface, (255,0,0), ceil_rect)

        self.bg_surface.blit(maze_surface, (
            self.minimap_grid_size[0] // 2 * self.bg_cell_size, self.minimap_grid_size[1] // 2 * self.bg_cell_size))

    def set_start_pos(self):
        for i in range(self.maze_row):
            for j in range(self.maze_col):
                if self.maze_toString[i][j] == 'S':
                    self.start_pos = (i, j)
                elif self.maze_toString[i][j] == 'E':
                    self.end_pos = (i, j)

    def visualize_maze(self, screen, solution_flag):
        copy_screen = screen.copy()

        if solution_flag:
            copy_screen = self.show_solution(copy_screen)

        copy_screen = self.draw_player(copy_screen)

        self.screen.blit(copy_screen, (RESOLUTION[0] - self.visual_maze_resolution[0], 0))

    def draw_player(self, screen):
        copy_visual_maze = self.visual_maze.copy()

        copy_visual_maze.blit(pygame.transform.scale_by(self.player.avatar, self.cell_size / self.minimap.cell_size),
                             (self.player.grid_pos[0] * self.cell_size, self.player.grid_pos[1] * self.cell_size))

        return copy_visual_maze

    def update_screen(self):
        self.minimap.update(self.minimap.maze_surface)
        self.visualize_maze(self.visual_maze, self.solution_flag)
    
    def auto_move(self):
        # Get the direction of the next move
        def get_direction(pos1, pos2):
            dx = pos2[0] - pos1[0]
            dy = pos2[1] - pos1[1]

            if dx > 0:
                return "DOWN"
            elif dx < 0:
                return "UP"
            elif dy < 0:
                return "LEFT"
            elif dy > 0:
                return "RIGHT"
            return "UP"
        # Create custom pygame event
        auto_event = pygame.event.Event(pygame.USEREVENT, key = None)
        move_list = {
            "UP": pygame.K_w,
            "DOWN": pygame.K_s,
            "LEFT": pygame.K_a,
            "RIGHT": pygame.K_d,
        }
        
        if not self.trace_path:
            return
        
        if self.auto_index < len(self.trace_path) - 1:
            direction = get_direction(self.trace_path[self.auto_index], self.trace_path[self.auto_index + 1])
            auto_event.key = move_list[direction]
            self.auto_index += 1
        else:
            direction = get_direction(self.trace_path[-1], self.end_pos)
            auto_event.key = move_list[direction]
         
        pygame.event.post(auto_event)
        pygame.event.post(auto_event)
        
    def init_panel(self):
        # INSTANTIATE PANELS
        tp.init(self.screen, tp.theme_game1)
        self.escape_buttons = [tp.Button("Resume"), 
                               tp.Button("Restart"), 
                               tp.Button("Save"),
                               tp.Button("Menu"), 
                               tp.Button("Quit")]
        # [MASK], Use to recognize whether the escape buttons is pressed
        self.associated_values = np.full((5,), 0).tolist()
        
        self.escape_box = tp.TitleBox("Settings", self.escape_buttons)
        self.escape_box.center_on(self.screen)

        def click_resume():
            self.associated_values[0] = 1
        def click_restart():
            self.associated_values[1] = 1
        def click_save():
            self.associated_values[2] = 1
        def click_menu():
            self.associated_values[3] = 1
        def click_quit():
            self.associated_values[4] = 1
            
        self.escape_buttons[0].at_unclick = click_resume
        self.escape_buttons[1].at_unclick = click_restart
        self.escape_buttons[2].at_unclick = click_save
        self.escape_buttons[3].at_unclick = click_menu
        self.escape_buttons[4].at_unclick = click_quit

        def before_gui():  # add here the things to do each frame before blitting gui elements
            self.screen.fill((250,) * 3)

        tp.call_before_gui(before_gui)  # tells thorpy to call before_gui() before drawing gui.

    def toggle_panel(self):
        pygame.event.clear()

        def at_refresh():
            copy_screen = self.screen.copy()
            copy_screen.blit(self.minimap.new_background, self.minimap.display_pos, (self.minimap.cut_start_pos, self.minimap.cut_area))
            copy_screen.blit(self.visual_maze, self.visual_maze_display_pos)
            self.blur = blur_screen(screen = copy_screen)
            
            self.screen.blit(self.blur, (0,0))

        self.player.deactivate(active=False)
        m = self.escape_box.get_updater(fps = FPS, esc_quit = True)
        at_refresh()
        # Stop spamming button 
        while m.playing:
            m.clock.tick(FPS)
            
            events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()

            m.update(events = events, mouse_rel = mouse_rel)
            pygame.display.flip()
            
            for event in events:
                if event.type == pygame.QUIT:
                    m.playing = False
                if event.type == pygame.KEYDOWN:
                    key_pressed = event.key
                    if key_pressed == pygame.K_ESCAPE:
                        self.player.deactivate(active = True)

                        self.screen.fill((0,0,0))
                        self.update_screen()
                        pygame.display.update()
                        
                        return None, None
                
                if self.associated_values[0]: #If click resume button
                    pygame.event.clear()

                    self.associated_values[0] = 0                    
                    self.player.deactivate(active = True)

                    self.update_screen()
                    pygame.display.update()

                    return None, None
                
                if self.associated_values[1]: # If click restart button
                    pass
                if self.associated_values[2]: # If click save button
                    pass  
                if self.associated_values[3]: # If click menu button
                    self.player.deactivate(active = True)

                    return "Menu", SCENES["Menu"]["initial_pos"]
                if self.associated_values[4]: # If click quit button
                    sys.exit(0)
                    pygame.quit()
        
        return None, None
    
    def init_choose_mode(self):
        choose_mode_choices = ("Manual", "Auto Mode")
        choose_mode = tp.AlertWithChoices("Choose Mode", choose_mode_choices, choice_mode="v")
        choose_mode.set_topleft(890, 500)
        
        manual_choices = ("On", "Off") 
        manual_mode = tp.AlertWithChoices("", manual_choices, choice_mode="v")
        manual_mode.set_topleft(957, 485)
        
        auto_choices = ("BFS", "DFS", "A*", "Greedy", "Dijkstra")
        auto_options = tp.AlertWithChoices("Auto Mode Algorithm", auto_choices, choice_mode="v")
        auto_options.set_topleft(880, 500)
        
        def create_background(): # Ham fix cai background, khong co gi trong day
            pass
        def choose_mode_background():
            self.screen.blit(self.minimap.new_background, self.minimap.display_pos, (self.minimap.cut_start_pos, self.minimap.cut_area))
        def click_choose_mode():
            choose_mode.launch_alone(choose_mode_background)
            
            if choose_mode.choice == "Manual":
                self.choose_mode_flag = False
                self.manual_flag = True
                
                self.player.deactivate(active=True)
            elif choose_mode.choice == "Auto Mode":
                self.choose_mode_flag = False
                self.auto_flag = True
                
                self.solution_flag = True
                self.minimap.solution_flag = True
                
                self.player.deactivate(active=True)
            
            self.screen.fill((0,0,0))
            # self.auto_button.update(events)
            self.update_screen()
            
            pygame.display.update()
        def click_hint():
            manual_mode.launch_alone(create_background)
            
            if manual_mode.choice == "On":
                self.solution_flag = True
                self.minimap.solution_flag = True
                self.update_screen()
                pygame.display.update()
            elif manual_mode.choice == "Off":
                self.solution_flag = False
                self.minimap.solution_flag = False
            
            self.screen.fill((0,0,0))
            # self.auto_button.update(events)
            self.update_screen()
            
            pygame.display.update()
            
        # Run when click auto
        def click_auto():
            auto_options.launch_alone(create_background)
            pygame.event.clear()
            
            if not auto_options.choice or auto_options.choice == 'BFS':
                self.trace_path, _ = self.algorithms.bfs(self.player.grid_pos[::-1], self.end_pos)
                self.auto_index = 0
            elif auto_options.choice == 'DFS':
                self.trace_path, _ = self.algorithms.dfs(self.player.grid_pos[::-1], self.end_pos)
                self.auto_index = 0
            elif auto_options.choice == 'A*':
                self.trace_path, _ = self.algorithms.a_star(self.player.grid_pos[::-1], self.end_pos)
                self.auto_index = 0
            elif auto_options.choice == 'Greedy':
                self.trace_path, _ = self.algorithms.greedy(self.player.grid_pos[::-1], self.end_pos)
                self.auto_index = 0
            elif auto_options.choice == 'Dijkstra':
                self.trace_path, _ = self.algorithms.dijkstra(self.player.grid_pos[::-1], self.end_pos)
                self.auto_index = 0
            
            self.screen.fill((0,0,0))
            # self.auto_button.update(events)
            self.update_screen()
            
            pygame.display.update()
            
        self.choose_mode = tp.Button("Mode")
        self.choose_mode.set_topleft((RESOLUTION[1] + RESOLUTION[0]) // 2 - 50, RESOLUTION[1] // 2 + 50)
        self.choose_mode.at_unclick = click_choose_mode
        
        self.hint_button = tp.Button("Show Hint")
        self.hint_button.set_topleft((RESOLUTION[1] + RESOLUTION[0]) // 2 - 50, RESOLUTION[1] // 2 + 50)
        self.hint_button.at_unclick = click_hint
        
        self.auto_button = tp.Button("Auto Mode")
        self.auto_button.set_topleft((RESOLUTION[1] + RESOLUTION[0]) // 2 - 50, RESOLUTION[1] // 2 + 50)
        self.auto_button.at_unclick = click_auto
    
    def show_solution(self, screen):
        copy_screen = screen.copy()

        self.minimap.trace_path, _ = self.algorithms.a_star(self.player.grid_pos[::-1], self.end_pos)
        
        if not self.minimap.trace_path:
            return screen
        
        self.minimap.trace_path.append(self.end_pos)
        
        color = (127,0,255)
            
        for pos in self.minimap.trace_path[:-1]:
            ceil_rect = pygame.Rect(pos[1] * self.cell_size, pos[0] * self.cell_size, self.cell_size, self.cell_size)

            pygame.draw.rect(copy_screen, color, ceil_rect)
            
        return copy_screen
    
    def draw_player(self, screen):
        copy_screen = screen.copy()

        copy_screen.blit(pygame.transform.scale_by(self.player.avatar, self.cell_size / self.minimap.cell_size), 
                         (self.player.grid_pos[0] * self.cell_size, self.player.grid_pos[1] * self.cell_size))

        return copy_screen
             
# screen = pygame.display.set_mode((1300, 900))
# test = Gameplay(screen, (0,0), (9, 9))
# test.play()
