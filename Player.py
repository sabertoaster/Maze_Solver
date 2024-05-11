from copy import deepcopy

import numpy as np
import pygame
from GridMapObject import GridMapObject as Gmo
from Visualize.ImageProcess import morph_image
from Visualize.TextBox import TextBox   
from pygame_textinput import TextInputManager, TextInputVisualizer

from CONSTANTS import SCENES, RESOLUTION, RESOURCE_PATH, AVATAR, MOVEMENT


class Player:
    """
    This is a class to represent Player Instance
    """

    def __init__(self, screen, grid_map, current_scene, initial_pos, skin="blackTom", player_name='Guest'):

        """
        :param screen:
        :param grid_map:
        :param current_scene:
        """
        self.door_pos = None

        self.active = True
        self.screen = screen
        self.current_scene = current_scene

        self.grid_map = grid_map

        self.skin = skin
        self.avatar = morph_image(RESOURCE_PATH + AVATAR[self.skin]["down"], SCENES[self.current_scene]["cell"])

        self.ratio = (RESOLUTION[0] // SCENES[self.current_scene]["cell"][0], RESOLUTION[1] // SCENES[self.current_scene]["cell"][1])

        self.grid_pos = initial_pos  # [PROTOTYPE]
        self.visual_pos = (self.grid_pos[0] * SCENES[self.current_scene]["cell"][0], self.grid_pos[1] * SCENES[self.current_scene]["cell"][1])
        self.grid_step = 1
        self.visual_step = self.grid_step * SCENES[self.current_scene]["cell"][0]
        self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.PLAYER
        
        self.name = player_name

        self.name_box = TextBox(screen=self.screen,
                                position=(0, 0, SCENES[self.current_scene]["cell"][0] * 2, SCENES[self.current_scene]["cell"][1]),
                                font_color=(0, 0, 0),
                                manager=TextInputManager(),
                                text=self.name)

        self.name_length = self.name_box.get_length()

        self.visualize_direction = (deepcopy(self.visual_pos), deepcopy(self.visual_pos))

    def set_current_scene(self, target_scene, initial_pos):
        """
        Set current scene
        :return:
        """
        self.current_scene = target_scene

        self.avatar = morph_image(RESOURCE_PATH + AVATAR[self.skin]["down"], SCENES[target_scene]["cell"])  # [PROTOTYPE]
        print(self.grid_map.get_map(self.current_scene).get_grid())
        self.avatar = morph_image(RESOURCE_PATH + AVATAR[self.skin]["down"], SCENES[target_scene]["cell"])  # [PROTOTYPE]
        self.ratio = (RESOLUTION[0] // SCENES[target_scene]["cell"][0], RESOLUTION[1] // SCENES[target_scene]["cell"][1])

        self.grid_pos = initial_pos  # [PROTOTYPE]
        self.visual_pos = (self.grid_pos[0] * SCENES[target_scene]["cell"][0], self.grid_pos[1] * SCENES[target_scene]["cell"][1])
        self.grid_step = 1
        self.visual_step = self.grid_step * SCENES[self.current_scene]["cell"][0]
        self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.PLAYER

        self.visualize_direction = (deepcopy(self.visual_pos), deepcopy(self.visual_pos))

    def set_current_door(self, pos):
        self.door_pos = pos

    def get_current_door(self):
        return self.door_pos

    def handle_event(self, key_pressed):
        """
        Handle event from keyboard
        :param key_pressed:
        :return:
        """
        # NEED OPTIMIZE HERE
        if self.active:
            response = None
            if key_pressed == pygame.K_RIGHT or key_pressed == pygame.K_d:
                response = self.move("right")
                self.avatar = morph_image(RESOURCE_PATH + AVATAR[self.skin]["right"], resolution=SCENES[self.current_scene]["cell"])
            if key_pressed == pygame.K_LEFT or key_pressed == pygame.K_a:
                response = self.move("left")
                self.avatar = morph_image(RESOURCE_PATH + AVATAR[self.skin]["left"], resolution=SCENES[self.current_scene]["cell"])
            if key_pressed == pygame.K_DOWN or key_pressed == pygame.K_s:
                response = self.move("down")
                self.avatar = morph_image(RESOURCE_PATH + AVATAR[self.skin]["down"], resolution=SCENES[self.current_scene]["cell"])
            if key_pressed == pygame.K_UP or key_pressed == pygame.K_w:
                response = self.move("up")
                self.avatar = morph_image(RESOURCE_PATH + AVATAR[self.skin]["up"], resolution=SCENES[self.current_scene]["cell"])
            if key_pressed == pygame.K_e:
                self.interact()
                return "Interact"
            pygame.event.clear()
            print("Response: ", response)
            return response
        return None

    def update(self, screenCopy):
        """
        Update player position
        :param screenCopy:
        :return:
        """
        
        self.screen.blit(screenCopy.copy(), (0, 0))
        self.draw(screenCopy)

    def re_init(self, name, scene):
        self.current_scene = scene
        self.name = name

        self.name_box = TextBox(screen=self.screen,
                                position=(0, 0, SCENES[self.current_scene]["cell"][0] * 2, SCENES[self.current_scene]["cell"][1]),
                                font_color=(0, 0, 0),
                                manager=TextInputManager(),
                                text=self.name)

        self.name_length = self.name_box.get_length()     
           
    def draw(self, screenCopy):
        """
        Draw player
        :return:
        """
        
        copy_scr = screenCopy.copy()
        if self.active:
            if self.visualize_direction[0] != self.visualize_direction[1]:
                rate = 100
                for i in range(0, rate):
                    self.visual_pos = (self.visual_pos[0] + (self.visualize_direction[1][0] - self.visualize_direction[0][0]) * self.grid_step * 1 / rate,
                                       self.visual_pos[1] + (self.visualize_direction[1][1] - self.visualize_direction[0][1]) * self.grid_step * 1 / rate)


                    if i % 4 == 0:
                        self.screen.blit(self.avatar, self.visual_pos)
                        self.name_box.set_position((self.visual_pos[0] - (self.name_length // 2) + (SCENES[self.current_scene]["cell"][0] // 2),
                                                    self.visual_pos[1] - SCENES[self.current_scene]["cell"][0] * 1.5))
                        self.name_box.draw(True)
                        pygame.time.delay(1)
                        pygame.display.flip()
                        self.screen.blit(copy_scr, (0, 0))
                self.visualize_direction = (self.visualize_direction[1], self.visualize_direction[1])
                return
            
            self.screen.blit(self.avatar, self.visual_pos)
            self.name_box.set_position((self.visual_pos[0] - (self.name_length//2) + (SCENES[self.current_scene]["cell"][0]//2), self.visual_pos[1] - SCENES[self.current_scene]["cell"][0]*1.5))
            self.name_box.draw(True)
            pygame.display.flip()

    def move(self, cmd):
        """
        Move player
        :param cmd:
        :return:
        """
        status = self.is_legal_move(cmd)
        if status != Gmo.WALL:
            x, y = MOVEMENT[cmd]
            self.visualize_direction = (deepcopy(self.visual_pos), deepcopy(
                (self.visual_pos[0] + x * self.visual_step, self.visual_pos[1] + y * self.visual_step)))

            if status == Gmo.DOOR:
                self.set_current_door((self.grid_pos[0] + x, self.grid_pos[1] + y))
                return "Door"

            if cmd in MOVEMENT and self.active:
                self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.FREE
                self.grid_pos = (self.grid_pos[0] + x, self.grid_pos[1] + y)
                # self.visual_pos = (self.visual_pos[0] + x * self.visual_step, self.visual_pos[1] + y * self.visual_step)
                self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.PLAYER

            return "Move"

    def is_legal_move(self, cmd):
        """
        Check if the move is legal
        :param cmd:
        :return:
        """
        x, y = MOVEMENT[cmd]

        if (0 <= self.grid_pos[0] + x < self.ratio[0]) and (0 <= self.grid_pos[1] + y < self.ratio[1]):
            return self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1] + y][
                self.grid_pos[0] + x]

        return Gmo.WALL

    def get_grid_pos(self):
        """
        Get self grid position
        :return:
        """
        return self.grid_pos

    def get_GridMapObject_Player(self, scene):
        """
        Get GridMapObject.PLAYER
        :return:
        """
        grid = self.grid_map.get_map(scene).get_grid()
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == Gmo.PLAYER:
                    return j, i

    def deactivate(self, active):
        """
        Deactivate player movement and stuff
        :return:
        """
        self.active = active

    def interact(self):
        """
        Interact with the environment
        :return:
        """
        pass
