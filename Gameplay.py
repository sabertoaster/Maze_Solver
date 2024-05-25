# Custom imports
from Algorithms.Algorithms import *
from Algorithms.MazeGeneration import Maze, convert as convert_maze, convert_energy
from GridMapObject import GridMapObject
from GridMap import GridMap
from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, FPS
RESOURCE_PATH += 'img/'

import os
import sys
import pygame
import numpy as np
import json
import thorpy as tp
from Visualize.ImageProcess import blur_screen, morph_image
from Visualize.TextBox import FormManager, Color
from Visualize.Transition import Transition
from Minimap import Minimap
from Player import *
from random import shuffle
import time
from Visualize.WinScreen import WinScreen

SCENE_NAME = "Gameplay"

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
        self.start_time = 0
        self.maze_time = 0
        self.maze_score = 0
        self.maze_step = 0
        self.maze_id = -1
        # INSTANTIATE SAVE FLAGS
        self.save_fl = False
        self.old_save = False

        self.minimap_grid_size = (20, 20)
        SCENES["Gameplay"]["cell"] = (RESOLUTION[1] // self.minimap_grid_size[0], RESOLUTION[1] // self.minimap_grid_size[0])

        self.sounds_handler = sounds_handler    
        
        self.win_screen = WinScreen(self.screen, self.sounds_handler)
        
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
                self.old_save = True
                self.maze_toString = data["maze_toString"]
                self.old_save = True
                self.maze_step = data["step"]
                self.maze_time = data["time"]
                self.maze_id = data["id"]
            else:
                self.maze = Maze("Wilson", self.maze_size)
                self.maze_toString = convert_maze(self.maze)

    def save_data(self, is_win=False):
        snapshot = self.minimap.get_snapshot()
        if is_win:
            if self.old_save:
                with open("SaveFile\\" + self.player.name + ".json", "r+") as fi:
                    file_data = json.load(fi)
                    for i in range(len(file_data)):
                        if file_data[i]["id"] == self.maze_id:
                            file_data.pop(i)
                            os.remove("SaveFile\\" + self.player.name + str(self.maze_id) + ".png")
                            break
                    fi.seek(0)
                    open("SaveFile\\" + self.player.name + ".json", 'w').close()
                    json.dump(file_data, fi, indent=4)
                return

            data = {
                "player.name": self.player.name,
                "player.grid_pos": self.player.grid_pos,
                "player.visual_pos": self.player.visual_pos,
                "level": self.maze_level,
                "mode": self.maze_mode,
                "score": round(self.maze_time, 2) if (is_win and round(self.maze_time, 2) < self.maze_score) or (
                            self.maze_score == 0 and is_win) else self.maze_score,
                "time": round(self.maze_time, 2),
                "step": self.maze_step,
                "maze_toString": self.maze_toString
            }

            try:
                with open("WinRecord\\" + self.player.name + ".json", "r+") as fi:
                    try:
                        file_data = json.load(fi)
                        self.maze_id = file_data[-1]["id"] + 1
                        data["id"] = self.maze_id
                        file_data.append(data)
                    except json.JSONDecodeError:
                        data["id"] = 0
                        file_data = [data]
                    fi.seek(0)
                    open("WinRecord\\" + self.player.name + ".json", 'w').close()
                    json.dump(file_data, fi, indent=4)
            except FileNotFoundError:
                with open("WinRecord\\" + self.player.name + ".json", "w+") as fi:
                    data["id"] = 0
                    json.dump([data], fi, indent=4)
            return

        if self.old_save:
            data = {
                "player.name": self.player.name,
                "player.grid_pos": self.player.grid_pos,
                "player.visual_pos": self.player.visual_pos,
                "level": self.maze_level,
                "mode": self.maze_mode,
                "score": round(self.maze_time, 2) if (is_win and round(self.maze_time, 2) < self.maze_score) or (self.maze_score == 0 and is_win) else self.maze_score,
                "time": round(self.maze_time, 2),
                "step": self.maze_step,
                "maze_toString": self.maze_toString
            }
            with open("SaveFile\\" + self.player.name + ".json", "r+") as fi:
                try:
                    file_data = json.load(fi)

                    data["id"] = self.maze_id
                    file_data[self.maze_id] = data
                except json.JSONDecodeError:
                    file_data = [data]
                fi.seek(0)
                open("SaveFile\\" + self.player.name + ".json", 'w').close()
                json.dump(file_data, fi, indent=4)
                pygame.image.save(snapshot, "SaveFile\\" + self.player.name + str(data["id"]) + ".png")
            return


        if not self.save_fl:
            data = {
                "player.name": self.player.name,
                "player.grid_pos": self.player.grid_pos,
                "player.visual_pos": self.player.visual_pos,
                "level": self.maze_level,
                "mode": self.maze_mode,
                "score": round(self.maze_time, 2) if (is_win and round(self.maze_time, 2) < self.maze_score) or (self.maze_score == 0 and is_win) else self.maze_score,
                "time": round(self.maze_time, 2), 
                "step": self.maze_step,
                "maze_toString": self.maze_toString
            }

            try:
                with open("SaveFile\\" + self.player.name + ".json", "r+") as fi:
                    try:
                        file_data = json.load(fi)
                        self.maze_id = file_data[-1]["id"] + 1
                        data["id"] = self.maze_id
                        file_data.append(data)
                        if len(file_data) > 3: # Xoa bot file save
                            file_data.pop(0)
                    except json.JSONDecodeError:
                        data["id"] = 0
                        file_data = [data]
                    fi.seek(0)
                    open("SaveFile\\" + self.player.name + ".json", 'w').close()
                    json.dump(file_data, fi, indent=4)
                    pygame.image.save(snapshot, "SaveFile\\" + self.player.name + str(data["id"]) + ".png")
            except FileNotFoundError:
               with open("SaveFile\\" + self.player.name + ".json", "w+") as fi:
                    data["id"] = 0
                    json.dump([data], fi, indent=4)
                    pygame.image.save(snapshot, "SaveFile\\" + self.player.name + str(data["id"]) + ".png")

        else:
            data = {
                "player.name": self.player.name,
                "player.grid_pos": self.player.grid_pos,
                "player.visual_pos": self.player.visual_pos,
                "level": self.maze_level,
                "mode": self.maze_mode,
                "score": round(self.maze_time, 2) if (is_win and round(self.maze_time, 2) < self.maze_score) or (self.maze_score == 0 and is_win) else self.maze_score,
                "time": round(self.maze_time, 2),
                "step": self.maze_step,
                "maze_toString": self.maze_toString
            }
            with open("SaveFile\\" + self.player.name + ".json", "r+") as fi:
                try:
                    file_data = json.load(fi)
                    data["id"] = self.maze_id
                    file_data[-1] = (data)
                except json.JSONDecodeError:
                    file_data = [data]
                fi.seek(0)
                open("SaveFile\\" + self.player.name + ".json", 'w').close()
                json.dump(file_data, fi, indent=4)
                pygame.image.save(snapshot, "SaveFile\\" + self.player.name + str(data["id"]) + ".png")

        # json.dump(data, fi, indent=4)
        # except:
        #     with open(self.player.name + ".json", "w+") as fi:

    def update_time(self):
        current_time = time.time()
        self.maze_time += float(current_time - self.start_time)
        self.start_time = current_time
        self.visualize_time_and_step()

    def play(self, player):
        self.player = player
        # Flag: có chọn mode energy không
        self.energy_flag = True
        # Khoi tao nang luong cho player
        self.energy = np.random.randint(5, 11)
        print("init energy", self.energy)
        self.get_data()

        # INSTANTIATE MAZE

        # VISUALIZE TIME AND STEPS
        self.text_box = FormManager(self.screen, {
            "time": {"position": (900, 600, 568, 30), "color": Color.RED.value, "maximum_length": 16,
                         "focusable": False, "init_text": ""},  # (x, y, width, height)
            "step": {"position": (900, 700, 568, 30), "color": Color.RED.value, "maximum_length": 16,
                         "focusable": False, "init_text": ""}})  # (x, y, width, height)

        # Chuyển từ dạng string sang maze dạng string nhưng mỗi ô chứa năng lượng thay vì ' ' sẽ chứa số từ 1 -> 5 (str type)
        if self.energy_flag:
            self.maze_toString = convert_energy(self.maze_toString)
        self.init_maze()

    
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
            self.visualize_time_and_step()
            events = pygame.event.get()
            mouse_rel = pygame.mouse.get_rel()

            if self.choose_mode_flag:
                choose_mode_launcher.update(events=events, mouse_rel=mouse_rel)
            elif self.manual_flag:
                manual_launcher.update(events=events, mouse_rel=mouse_rel)
            elif self.auto_flag:
                self.auto_move()

                # Block player keyboard input

                auto_launcher.update(events=events, mouse_rel=mouse_rel)

            self.update_time() if self.manual_flag else None
            for event in events:
                if event.type == pygame.QUIT:
                    return None, None
                if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
 
                    if event.key == pygame.K_m:
                        self.sounds_handler.switch()
                        continue
                    
                    if event.key == pygame.K_ESCAPE:
                        if self.manual_flag:
                            start_pause_time = time.time()
                            end_pause_time = time.time()
                            pause_time = float(end_pause_time - start_pause_time)
                            self.maze_time -= pause_time
                            pygame.key.set_repeat(200, 125)
                        pygame.key.set_repeat()
                        next_scene, next_pos = self.toggle_panel()
                        if next_scene:
                            return next_scene, next_pos

                        break
                        
                    if event.key == pygame.K_g:
                        pass
                        # save = SaveFile(self.maze_toString, self.player)
                        # save.run_save('test1')
                        
                        # Handle minimap here
                        
                    player_response = self.player.handle_event(event.key)
                    
                    if player_response == "Move" or event.type == pygame.USEREVENT:
                        self.maze_step += 1
                        
                        #Xử lí năng lượng
                        self.energy -= 1 # Mỗi bước đi -1 energy
                        #Nếu player đi qua ô có năng lượng
                        if self.maze_toString[self.player.grid_pos[1]][self.player.grid_pos[0]].isnumeric():
                            # Cộng thêm năng lượng cho player
                            self.energy += int(self.maze_toString[self.player.grid_pos[1]][self.player.grid_pos[0]])
                            # Bỏ năng lượng tại ô đó
                            self.maze_toString[self.player.grid_pos[1]][self.player.grid_pos[0]] = ' '
                            
                        print("energy", self.energy)
                        
                        if self.player.get_grid_pos()[::-1] == self.end_pos:
                            if self.auto_flag != True:
                                self.save_data(is_win=True)

                            scene_name, initial_pos = self.finish_game_panel()
                            if scene_name:
                                return scene_name, initial_pos
                        pygame.event.clear()
                        
                        if self.energy <= 0: # xu li thua
                            pass
                        
                    # if self.solution_flag:
                    #     ceil_rect = pygame.Rect(self.player.grid_pos[0] * self.cell_size, self.player.grid_pos[1] * self.cell_size, self.cell_size, self.cell_size) # [PROTOTYPE]
                    #     pygame.draw.rect(self.visual_maze, (255,255,255), ceil_rect)
                    
                    self.update_screen()
                    
                pygame.display.update()

    # def update_maze(self):
    #     if self.file_name == '':
    #         self.maze = Maze("Wilson", self.maze_size)
    #         self.maze_toString = convert_maze(self.maze)
    #     else:
    #         data = read_file(self.file_name)
    #         self.maze_toString = data['maze_toString']

    def finish_game_panel(self):
        
        current_frame = self.screen.copy()
        blur = blur_screen(current_frame)
        self.win_screen.play(background=blur)
        
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return None, None
                
                mouse_pos = pygame.mouse.get_pos()
                mouse_grid_pos = (mouse_pos[1] // SCENES[SCENE_NAME]['cell'][0]), (
                            mouse_pos[0] // SCENES[SCENE_NAME]['cell'][1])
                
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    if event.key == pygame.K_m:
                        running = False
                        return "Menu", SCENES["Menu"]["initial_pos"]
                    else:
                        running = False
                        return "Gameplay", SCENES["Gameplay"]["initial_pos"]

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
                    
                if self.energy_flag: #Nếu có chọn mode energy
                    if self.maze_toString[i][j].isnumeric():
                        # Xử lí các ô năng lượng
                        if self.maze_toString[i][j] == '1':
                            color = (84, 245, 66)
                        elif self.maze_toString[i][j] == '2':
                            color = (66, 245, 152)
                        elif self.maze_toString[i][j] == '3':
                            color = (66, 245, 239)
                        elif self.maze_toString[i][j] == '4':
                            color = (66, 129, 245)
                        elif self.maze_toString[i][j] == '5':
                            color = (129, 66, 245)
                        pygame.draw.rect(self.visual_maze, color, ceil_rect)

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

        self.bg_surface = morph_image(RESOURCE_PATH + "nigga.png", screen_size)

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
        rand = list(range(0, len(walls)))
        shuffle(rand)
        index = 0
        for i in range(self.maze_row):
            for j in range(self.maze_col):
                pos = (j * self.bg_cell_size, i * self.bg_cell_size)

                if self.maze_toString[i][j] == '#':
                    # img = pygame.image.load(RESOURCE_PATH + walls[np.random.randint(0, len(walls))]).convert_alpha()
                    img = morph_image(RESOURCE_PATH + walls[rand[index]],
                                      (self.bg_cell_size, self.bg_cell_size * 2))
                    maze_surface.blit(img, pos)
                    
                    index += 1
                    if index == len(walls):
                        shuffle(rand)
                        index = 0

                elif self.maze_toString[i][j] == 'S':

                    maze_surface.blit(start,
                                      (pos[0] + (self.bg_cell_size - start.get_width()) / 2,
                                            pos[1] + (self.bg_cell_size - start.get_height()) / 2))

                elif self.maze_toString[i][j] == 'E':
                    maze_surface.blit(end, pos)
                
                if self.energy_flag: # Xử lí năng lượng
                    if self.maze_toString[i][j].isnumeric():
                        if self.maze_toString[i][j] =='1':
                            pass
                        elif self.maze_toString[i][j] =='2':
                            pass
                        elif self.maze_toString[i][j] =='3':
                            pass
                        elif self.maze_toString[i][j] =='4':
                            pass
                        elif self.maze_toString[i][j] =='5':
                            pass

        self.bg_surface.blit(maze_surface,((screen_size[0] - maze_surface.get_width()) // 2, (screen_size[1] - maze_surface.get_height()) // 2))

    def set_start_pos(self):
        if self.old_save == True:
            self.start_pos = self.player.grid_pos[::-1]
            for i in range(self.maze_row):
                for j in range(self.maze_col):
                    if self.maze_toString[i][j] == 'E':
                        self.end_pos = (i, j)
                        break
            return
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
        self.screen.blit(copy_screen, (RESOLUTION[0] - copy_screen.get_width(), 0))
        
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
                        if not self.choose_mode_flag:
                            self.player.deactivate(active=True)

                        self.screen.fill((0,0,0))
                        self.update_screen()
                        pygame.display.update()
                        
                        return None, None

                if self.associated_values[0]: #If click resume button
                    pygame.event.clear()

                    self.associated_values[0] = 0
                    
                    if not self.choose_mode_flag:
                        self.player.deactivate(active = True)

                    self.update_screen()
                    pygame.display.update()

                    return None, None
                if self.associated_values[1]: #If click restart button
                    self.associated_values[1] = 0
                    return "Gameplay", SCENES["Gameplay"]["initial_pos"]
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
                    self.player.deactivate(active=True)

                    self.transition.transition(
                        pos=(SCENES["Menu"]["initial_pos"][0] * SCENES["Menu"]["cell"][0],
                             SCENES["Menu"]["initial_pos"][1] * SCENES["Menu"]["cell"][1]),
                        transition_type="reversed_hole",
                        next_scene="Menu")

                    return "Menu", SCENES["Menu"]["initial_pos"]

                if self.associated_values[4]: #If click quit button
                    pygame.quit()
                    exit()

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
                self.start_time = time.time()
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
        
        # Nếu chọn mode energy
        if self.energy_flag:        
            self.minimap.trace_path, _ = self.algorithms.path_energy(self.energy, self.player.grid_pos[::-1], self.end_pos)
        else:
            self.minimap.trace_path, _ = self.algorithms.a_star(self.player.grid_pos[::-1], self.end_pos)
            
        if self.minimap.trace_path:
            self.minimap.trace_path.append(self.end_pos)

        if not self.minimap.trace_path:
            return screen
        
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

    def visualize_time_and_step(self):
        self.text_box.set_text("time", str(round(self.maze_time, 2)))
        self.text_box.set_text("step", str(self.maze_step))

        self.text_box.get_textbox("time").draw(background=True)
        self.text_box.get_textbox("step").draw(background=True)
        pygame.display.flip()
# screen = pygame.display.set_mode((1300, 900))
# test = Gameplay(screen, (0,0), (9, 9))
# test.play()
