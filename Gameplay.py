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

SCENE_NAME = "GamePlay"

class Gameplay:
    def __init__(self, screen, start_pos, end_pos, file_name='', maze_size=(20, 20), sounds_handler=None):
        self.screen = screen
        self.screenCopy = self.screen.copy()
        self.screen.fill((0, 0, 0))  # Black background [PROTOTYPE]
        self.file_name = file_name
        self.maze_size = maze_size
        # CURRENT_LEVEL.value["maze_size"]

        # INSTANTIATE PANELS
        self.init_panel()
        self.start_time = time.time()
        self.maze_time = 0
        self.maze_score = 0
        self.maze_step = 0
        # INSTANTIATE SAVE FLAGS
        self.save_fl = False

        self.minimap_grid_size = (20, 20)
        SCENES["Gameplay"]["cell"] = (RESOLUTION[1] // self.minimap_grid_size[0], RESOLUTION[1] // self.minimap_grid_size[0])

        self.sounds_handler = sounds_handler    
        
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
            self.player.grid_pos = data['player.grid_pos']
            self.player.visual_pos = data['player.visual_pos']
            self.maze_level = data['level']
            self.maze_mode = data['mode']
            self.maze_score = data["score"]
            self.maze_time = data["time"]

            if (data["level"] == "Easy"):
                self.maze_size = (10, 10)
                self.minimap_grid_size = (20, 20)

            elif (data["level"] == "Medium"):
                self.maze_size = (20, 20)
                self.minimap_grid_size = (20, 20)

            elif (data["level"] == "Hard"):
                self.maze_size = (50, 50)
                self.minimap_grid_size = (40, 40)

            SCENES["Gameplay"]["cell"] = (RESOLUTION[1] // self.minimap_grid_size[0], RESOLUTION[1] // self.minimap_grid_size[0])

            self.player.re_init(self.player.name, "Gameplay")
            if data["maze_toString"]:
                self.maze_toString = data["maze_toString"]

            else:
                self.maze = Maze("Wilson", self.maze_size)
                self.maze_toString = convert_maze(self.maze)

    def save_data(self, is_win=False):
        if not self.save_fl:
            data = {
                "player.name": self.player.name,
                "player.grid_pos": self.player.grid_pos,
                "player.visual_pos": self.player.visual_pos,
                "level": self.maze_level,
                "mode": self.maze_mode,
                "score": self.maze_score + 100 if is_win else self.maze_score,
                "time": round(self.maze_time, 2), 
                "step": self.maze_step,
                "maze_toString": self.maze_toString
            }
            try:
                with open("SaveFile\\" + self.player.name + ".json", "r+") as fi:
                    try:
                        file_data = json.load(fi)
                        data["id"] = len(file_data)
                        file_data.append(data)
                    except json.JSONDecodeError:
                        data["id"] = 0
                        file_data = [data]
                    fi.seek(0)
                    json.dump(file_data, fi, indent=4)
            except FileNotFoundError:
               with open("SaveFile\\" + self.player.name + ".json", "w+") as fi:
                    data["id"] = 0
                    json.dump([data], fi, indent=4)

        else:
            data = {
                "player.name": self.player.name,
                "player.grid_pos": self.player.grid_pos,
                "player.visual_pos": self.player.visual_pos,
                "level": self.maze_level,
                "mode": self.maze_mode,
                "score": self.maze_score + 100 if is_win else self.maze_score,
                "time": round(self.maze_time, 2),
                "step": self.maze_step,
                "maze_toString": self.maze_toString
            }
            with open("SaveFile\\" + self.player.name + ".json", "r+") as fi:
                try:
                    file_data = json.load(fi)
                    data["id"] = file_data[-1]["id"]
                    file_data[-1] = (data)
                except json.JSONDecodeError:
                    file_data = [data]
                fi.seek(0)
                json.dump(file_data, fi, indent=4)

        # json.dump(data, fi, indent=4)
        # except:
        #     with open(self.player.name + ".json", "w+") as fi:

    def update_time(self):
        current_time = time.time()
        self.maze_time += float(current_time - self.start_time)
        self.start_time = current_time
        
    def play(self, player):

        self.player = player
        self.get_data()

        # INSTANTIATE MAZE

        self.init_maze()
        print(self.visual_maze.get_size())

        # INSTANTIATE PLAYER
        self.set_start_pos()
        self.player.grid_pos = self.start_pos[::-1]
        # self.update_player()

        # INSTANTIATE ALGORITHMS
        self.algorithms = TotalAlgorithms(self.maze_toString)

        # INSTANTIATE BACKGROUND
        self.init_background()
        
        #play BGM
        self.sounds_handler.play_bgm(SCENE_NAME)



        # INSTANTIATE MINIMAP
        # minimap_display_pos = (0, (RESOLUTION[0] - RESOLUTION[1]) // 2)
        minimap_display_pos = (0, 0)
        self.minimap = Minimap(self.screen, self.maze_toString, self.minimap_grid_size, self.bg_surface.copy(),
                               self.bg_cell_size, minimap_display_pos, self.player)
        self.minimap.init_at_start(self.minimap.maze_surface)

        self.solution_flag = False


        self.visualize_maze(self.visual_maze, self.solution_flag)

        self.screenCopy = self.screen.copy()

        self.transition = Transition(self.screen, RESOLUTION, player=self.player, sounds_handler=self.sounds_handler)
        self.transition.transition(transition_type="hole",
                                   pos=(400, 400),
                                   prev_scene="Play")


        self.minimap.update(self.minimap.maze_surface)

        pygame.display.update()
        # self.minimap.update(self.screenCopy)
        # self.player.update(self.screenCopy)

        self.fill_grid_map()

        while True:
            self.update_time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None, None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # Disable spamming button
                        pygame.key.set_repeat()
                        start_pause_time = time.time()
                        next_scene, next_pos = self.toggle_panel()
                        # Enable spamming button again
                        end_pause_time = time.time()
                        pause_time = float(end_pause_time - start_pause_time)
                        self.maze_time -= pause_time
                        pygame.key.set_repeat(200, 125)

                        if next_scene:
                            return next_scene, next_pos

                        break
                    if event.key == pygame.K_m:
                        pass
                        # Handle minimap here
                    if event.key == pygame.K_x:
                        self.solution_flag = not self.solution_flag
                        self.minimap.solution_flag = not self.minimap.solution_flag

                        self.minimap.update(self.minimap.maze_surface)
                        self.visualize_maze(self.visual_maze, self.solution_flag)
                    if event.key == pygame.K_g:
                        pass
                        # save = SaveFile(self.maze_toString, self.player)
                        # save.run_save('test1')

                        # Handle minimap here
                    player_response = self.player.handle_event(event.key)
                    if player_response == "Move":
                        self.maze_step += 1
                        if self.player.get_grid_pos()[::-1] == self.end_pos:

                            self.save_data(is_win=True)
                            # return "Win", SCENES["Win"]["initial_pos"]
                        pygame.event.clear()
                    # if self.solution_flag:
                    #     ceil_rect = pygame.Rect(self.player.grid_pos[0] * self.cell_size, self.player.grid_pos[1] * self.cell_size, self.cell_size, self.cell_size) # [PROTOTYPE]
                    #     pygame.draw.rect(self.visual_maze, (255,255,255), ceil_rect)

                    self.minimap.update(self.minimap.maze_surface)
                    self.visualize_maze(self.visual_maze, self.solution_flag)

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
                ceil_rect = pygame.Rect(j * self.cell_size, i * self.cell_size, self.cell_size,
                                        self.cell_size)  # [PROTOTYPE]

                if self.maze_toString[i][j] == ' ':
                    pygame.draw.rect(self.visual_maze, (255, 255, 255), ceil_rect)
                elif self.maze_toString[i][j] == '#':
                    pygame.draw.rect(self.visual_maze, (0, 0, 0), ceil_rect)
                elif self.maze_toString[i][j] == 'S':
                    # self.start_pos = (i, j)
                    pygame.draw.rect(self.visual_maze, (170, 170, 0), ceil_rect)
                elif self.maze_toString[i][j] == 'E':
                    # self.end_pos = (i, j)
                    pygame.draw.rect(self.visual_maze, (255, 0, 0), ceil_rect)

        self.visual_maze_display_pos = (0, RESOLUTION[0] - (RESOLUTION[0] - RESOLUTION[1]) / 2)

        # test = convert_energy(self.maze_toString)
        # for i in range(len(test)):
        #     for j in range(len(test[0])):
        #         print(test[i][j], end='')
        #     print()

    def init_background(self):
        self.bg_cell_size = RESOLUTION[1] // self.minimap_grid_size[1]

        screen_size = ((self.maze_row + self.minimap_grid_size[0] + 1) * self.bg_cell_size,
                       (self.maze_col + self.minimap_grid_size[1] + 1) * self.bg_cell_size)

        self.bg_surface = morph_image("Resources/nigga.png", screen_size)

        maze_surface = pygame.Surface(((self.maze_row) * (self.bg_cell_size), ((self.maze_col) * self.bg_cell_size)),
                                      pygame.SRCALPHA, 32).convert_alpha()

        start = morph_image(RESOURCE_PATH + "start.png", (self.bg_cell_size, self.bg_cell_size))
        end = morph_image(RESOURCE_PATH + "jerry_icon.png", (self.bg_cell_size, self.bg_cell_size))
        walls = [
            "cave_wall_1.png",
            "cave_wall_2.png",
            "cave_wall_3.png",
            "cave_wall_4.png",
            "cave_wall_5.png",
            "cave_wall_6.png",
            "cave_wall_7.png",
            "cave_wall_8.png",
        ]
        for i in range(self.maze_row):
            for j in range(self.maze_col):
                pos = (j * self.bg_cell_size, i * self.bg_cell_size)
                if i == 0:
                    if j == 0:
                        floor = morph_image(RESOURCE_PATH + "floor_ul.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)
                    elif j == self.maze_row - 1:
                        floor = morph_image(RESOURCE_PATH + "floor_ur.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)
                    else:
                        floor = morph_image(RESOURCE_PATH + "floor_u.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)
                elif i == self.maze_col - 1:
                    if j == 0:
                        floor = morph_image(RESOURCE_PATH + "floor_dl.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)
                    elif j == self.maze_row - 1:
                        floor = morph_image(RESOURCE_PATH + "floor_dr.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)
                    else:
                        floor = morph_image(RESOURCE_PATH + "floor_d.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)
                else:
                    if j == 0:
                        floor = morph_image(RESOURCE_PATH + "floor_l.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)
                    elif j == self.maze_row - 1:
                        floor = morph_image(RESOURCE_PATH + "floor_r.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)
                    else:
                        floor = morph_image(RESOURCE_PATH + "floor.png", (self.bg_cell_size, self.bg_cell_size))
                        maze_surface.blit(floor, pos)

        for i in range(self.maze_row):
            for j in range(self.maze_col):
                pos = (j * self.bg_cell_size, i * self.bg_cell_size)

                if self.maze_toString[i][j] == '#':
                    # img = pygame.image.load(RESOURCE_PATH + walls[np.random.randint(0, len(walls))]).convert_alpha()
                    img = morph_image(RESOURCE_PATH + walls[np.random.randint(0, len(walls))],
                                      (self.bg_cell_size, self.bg_cell_size * 2))
                    maze_surface.blit(img, pos)

                elif self.maze_toString[i][j] == 'S':

                    maze_surface.blit(start,
                                      (pos[0] + (self.bg_cell_size - start.get_width()) / 2,
                                            pos[1] + (self.bg_cell_size - start.get_height()) / 2))

                elif self.maze_toString[i][j] == 'E':
                    maze_surface.blit(end, pos)

        self.bg_surface.blit(maze_surface,((screen_size[0] - maze_surface.get_width()) // 2, (screen_size[1] - maze_surface.get_height()) // 2))

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
        print(copy_screen.get_width(), copy_screen.get_height())
        self.screen.blit(copy_screen, (RESOLUTION[0] - copy_screen.get_width(), 0))


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
            self.blur = blur_screen(screen=copy_screen)

            self.screen.blit(self.blur, (0, 0))

        self.player.deactivate(active=False)
        m = self.escape_box.get_updater(fps=FPS, esc_quit=True)
        at_refresh()
        # Stop spamming button 
        while m.playing:
            m.clock.tick(FPS)

            events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()

            m.update(events=events, mouse_rel = mouse_rel)
            pygame.display.flip()

            for event in events:
                if event.type == pygame.QUIT:
                    m.playing = False
                if event.type == pygame.KEYDOWN:
                    key_pressed = event.key
                    if key_pressed == pygame.K_ESCAPE:
                        self.player.deactivate(active=True)

                        self.minimap.update(self.minimap.maze_surface)
                        self.visualize_maze(self.visual_maze, self.solution_flag)

                        return None, None

                if self.associated_values[0]: #If click resume button
                    pygame.event.clear()

                    self.associated_values[0] = 0
                    self.player.deactivate(active = True)

                    self.minimap.update(self.minimap.maze_surface)
                    self.visualize_maze(self.visual_maze, self.solution_flag)

                    return None, None

                if self.associated_values[1]: #If click restart button
                    pass
                if self.associated_values[2]: #If click save button
                    self.associated_values[2] = 0
                    self.save_data()
                    self.save_fl = True  # Set save flag to True
                    # if self.associated_values[3]: #If click auto button
                    # choices = ("BFS", "DFS", "A*", "Greedy", "Dijkstra")
                    # introduction_text = "Choose the algorithm to solve the maze"
                    # options = tp.AlertWithChoices("Auto Mode Algorithms", choices, introduction_text, choice_mode="v")
                    # def clicked():
                    #     options.launch_alone() #see _example_launch for more options
                    #     print("User has chosen:", options.choice)
                    # self.escape_buttons[3].center_on(self.screen)
                    # self.escape_buttons[3].at_unclick = clicked
                    # self.escape_buttons[3].get_updater(fps = FPS, esc_quit = True)
                    # return None, None

                if self.associated_values[3]: #If click menu button
                    self.player.deactivate(active = True)

                    return "Menu", SCENES["Menu"]["initial_pos"]

                if self.associated_values[4]: #If click quit button
                    pygame.quit()

        return None, None

    def show_solution(self, screen):
        copy_screen = screen.copy()

        self.minimap.trace_path, _ = self.algorithms.a_star(self.player.grid_pos[::-1], self.end_pos)
        if self.minimap.trace_path:
            self.minimap.trace_path.append(self.end_pos)

        if not self.minimap.trace_path:
            return screen

        color = (127, 0, 255)

        for pos in self.minimap.trace_path:
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
