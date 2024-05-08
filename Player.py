from copy import deepcopy

import numpy as np
import pygame
import cv2
from GridMapObject import GridMapObject as Gmo
from Visualize.ImageProcess import morph_image

AVATAR = {
    "Tom": {"down": "tom_icon_d.png",
            "right": "tom_icon_r.png",
            "left": "tom_icon_l.png",
            "up": "tom_icon_u.png"},
    
    "orangeTom": {"down": "orangeTom_icon_d.png",
                  "right": "orangeTom_icon_r.png",
                  "left": "orangeTom_icon_l.png",
                  "up": "orangeTom_icon_u.png"},

    "blackTom": {"down": "blackTom_icon_d.png",
                 "right": "blackTom_icon_r.png",
                 "left": "blackTom_icon_l.png",
                 "up": "blackTom_icon_u.png"},
}


class Player:
    """
    This is a class to represent Player Instance
    """

    def __init__(self, screen, res_cell, grid_map, current_scene, initial_pos, params, skin="blackTom"):

        """
        :param screen:
        :param res_cell:
        :param grid_map:
        :param current_scene:
        """
        from copy import deepcopy
        self.active = True
        self.screen = screen
        self.params = params
        resolution, cell = res_cell
        self.resolution = resolution
        self.cell_collection = cell
        self.grid_map = grid_map
        self.skin = skin
        self.movement = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }

        self.avatar = morph_image("Visualize/Resources/" + AVATAR[self.skin]["down"], res_cell[1][current_scene])  # [PROTOTYPE]
        self.current_scene = current_scene
        self.cell = cell[current_scene]
        self.ratio = (resolution[0] // cell[current_scene][0], resolution[1] // cell[current_scene][1])

        self.grid_pos = initial_pos  # [PROTOTYPE]
        self.visual_pos = (self.grid_pos[0] * cell[current_scene][0], self.grid_pos[1] * cell[current_scene][1])
        self.grid_step = 1
        self.visual_step = self.grid_step * cell[current_scene][0]
        self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.PLAYER

        self.visualize_direction = (deepcopy(self.visual_pos), deepcopy(self.visual_pos))

    def set_current_scene(self, target_scene, initial_pos):
        """
        Set current scene
        :return:
        """
        self.current_scene = target_scene

        self.cell = self.cell_collection[target_scene]
        self.avatar = morph_image("Visualize/Resources/" + AVATAR[self.skin]["down"], self.cell)  # [PROTOTYPE]
        print(self.grid_map.get_map(self.current_scene).get_grid())
        self.avatar = morph_image("Visualize/Resources/" + AVATAR[self.skin]["down"], self.cell)  # [PROTOTYPE]
        self.ratio = (self.resolution[0] // self.cell[0], self.resolution[1] // self.cell[1])

        self.grid_pos = initial_pos  # [PROTOTYPE]
        self.visual_pos = (self.grid_pos[0] * self.cell[0], self.grid_pos[1] * self.cell[1])
        self.grid_step = 1
        self.visual_step = self.grid_step * self.cell[0]
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
                self.avatar = morph_image("Visualize/Resources/" + AVATAR[self.skin]["right"], resolution=self.cell)
            if key_pressed == pygame.K_LEFT or key_pressed == pygame.K_a:
                response = self.move("left")
                self.avatar = morph_image("Visualize/Resources/" + AVATAR[self.skin]["left"], resolution=self.cell)
            if key_pressed == pygame.K_DOWN or key_pressed == pygame.K_s:
                response = self.move("down")
                self.avatar = morph_image("Visualize/Resources/" + AVATAR[self.skin]["down"], resolution=self.cell)
            if key_pressed == pygame.K_UP or key_pressed == pygame.K_w:
                response = self.move("up")
                self.avatar = morph_image("Visualize/Resources/" + AVATAR[self.skin]["up"], resolution=self.cell)
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

    def draw(self, screenCopy):
        """
        Draw player
        :return:
        """
        copy_scr = screenCopy.copy()
        if self.active:
            if self.visualize_direction[0] != self.visualize_direction[1]:
                for i in range(0, 24):
                    self.visual_pos = (self.visual_pos[0] + (self.visualize_direction[1][0] - self.visualize_direction[0][0]) * self.grid_step * 1 / 24,
                                       self.visual_pos[1] + (self.visualize_direction[1][1] - self.visualize_direction[0][1]) * self.grid_step * 1 / 24)
                    self.screen.blit(self.avatar, self.visual_pos)
                    pygame.time.delay(2)
                    if (i % 2 == 0):
                        pygame.display.flip()
                        pygame.time.wait(2)
                    self.screen.blit(copy_scr, (0, 0))
                    # pygame.display.flip()
                    # if ~(i % 5):
                    #     pygame.display.flip()
                    # pygame.time.delay(2)
                self.visualize_direction = (self.visualize_direction[1], self.visualize_direction[1])
                return
            self.screen.blit(self.avatar, self.visual_pos)
            pygame.display.flip()

    def move(self, cmd):
        """
        Move player
        :param cmd:
        :return:
        """
        status = self.is_legal_move(cmd)
        if status != Gmo.WALL:
            x, y = self.movement[cmd]
            self.visualize_direction = (deepcopy(self.visual_pos), deepcopy(
                (self.visual_pos[0] + x * self.visual_step, self.visual_pos[1] + y * self.visual_step)))

            if status == Gmo.DOOR:
                self.set_current_door((self.grid_pos[0] + x, self.grid_pos[1] + y))
                return "Door"

            if cmd in self.movement and self.active:
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
        x, y = self.movement[cmd]
        # print(self.grid_pos[0] + x, self.grid_pos[1] + y)
        # print(self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1] + y][self.grid_pos[0] + x])
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

    def distance_from_door(self):
        """
        return y, x position of grid_map
        return position of GridMapObject.FREE from self.grid_pos (must at door)
        """
        self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.DOOR
        cells = self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1] - 1:self.grid_pos[1] + 2, self.grid_pos[0] - 1:self.grid_pos[0] + 2]  # - set(self.grid_pos)
        relative_position = tuple([val.tolist()[0] - 1 for val in list(np.where(cells == Gmo.FREE))])

        return relative_position

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
