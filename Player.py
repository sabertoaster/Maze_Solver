import numpy as np
import pygame
import cv2
from GridMapObject import GridMapObject as Gmo
from Visualize.morph_image import morph_image

AVATAR = "tom_icon_1.png"


class Player:
    def __init__(self, screen, res_cell, grid_map, current_scene):
        self.avatar = morph_image("Visualize/Resources/" + AVATAR, res_cell[1])  # [PROTOTYPE]
        self.active = True
        self.screen = screen
        self.grid_map = grid_map
        self.current_scene = current_scene

        resolution, cell = res_cell
        self.ratio = (resolution[0] // cell[0], resolution[1] // cell[1])

        self.grid_pos = (12, 10)  # [PROTOTYPE]
        self.visual_pos = (self.grid_pos[0] * res_cell[1][0], self.grid_pos[1] * res_cell[1][1])
        self.grid_step = 1
        self.visual_step = self.grid_step * res_cell[1][0]

        self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.PLAYER

        self.movement = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }

    def handle_event(self, key_pressed):
        """
        Handle event from keyboard
        :param key_pressed:
        :return:
        """
        # NEED OPTIMIZE HERE
        if key_pressed[pygame.K_RIGHT] or key_pressed[pygame.K_d]:
            self.move("right")
        if key_pressed[pygame.K_LEFT] or key_pressed[pygame.K_a]:
            self.move("left")
        if key_pressed[pygame.K_DOWN] or key_pressed[pygame.K_s]:
            self.move("down")
        if key_pressed[pygame.K_UP] or key_pressed[pygame.K_w]:
            self.move("up")
        if key_pressed[pygame.K_e]:
            self.interact()
            return True
        return False

    def update(self, screenCopy):
        self.screen.blit(screenCopy, (0, 0))
        self.draw()

    def draw(self):
        if self.active:
            self.screen.blit(self.avatar, self.visual_pos)
        pygame.display.flip()

    def move(self, cmd):
        if cmd in self.movement and self.is_legal_move(cmd) and self.active:
            x, y = self.movement[cmd]
            self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.FREE
            self.grid_pos = (self.grid_pos[0] + x, self.grid_pos[1] + y)
            self.visual_pos = (self.visual_pos[0] + x * self.visual_step, self.visual_pos[1] + y * self.visual_step)
            self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1]][self.grid_pos[0]] = Gmo.PLAYER

    def is_legal_move(self, cmd):
        x, y = self.movement[cmd]
        # print(self.grid_pos[0] + x, self.grid_pos[1] + y)
        # print(self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1] + y][self.grid_pos[0] + x])
        if (0 <= self.grid_pos[0] + x < self.ratio[0]) and (0 <= self.grid_pos[1] + y < self.ratio[1]):
            return self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1] + y][
                self.grid_pos[0] + x] == Gmo.FREE or self.grid_map.get_map(self.current_scene).get_grid()[self.grid_pos[1] + y][
                self.grid_pos[0] + x] == Gmo.DOOR
        return False

    def get_grid_pos(self):
        return self.grid_pos

    def deactivate(self):
        self.active = not self.active

    def interact(self):
        pass
