import json
import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element
from Visualize.TextBox import TextBox, FormManager, Color
from Visualize.MouseEvents import MouseEvents
from Visualize.Transition import Transition
from Visualize.HangingSign import HangingSign

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS

SCENE_NAME = "Play"


def drawGrid(screen):
    """
    FOR FUCKING DEBUG THE GRID MAP
    :param screen:
    :return:
    """
    blockSize = SCENES[SCENE_NAME]["cell"][0]  # Set the size of the grid block
    for x in range(0, RESOLUTION[0], blockSize):
        for y in range(0, RESOLUTION[1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, COLORS.WHITE.value, rect, 1)


class PlayScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """

    def __init__(self, screen):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """
        self.panel_fl = False
        self.frame = morph_image(RESOURCE_PATH + SCENES[SCENE_NAME]["BG"], RESOLUTION)
        self.screen = screen

        # Transition effect
        self.transition = Transition(self.screen, RESOLUTION)

        self.sign = HangingSign(SCENE_NAME.upper(), 50)

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """

        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        pygame.display.flip()
        # drawGrid(screen=self.screen)

        self.player = player
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background

        load_panel = pygame.image.load(RESOURCE_PATH + "load_panel.png").convert_alpha()
        blur = blur_screen(screen=self.screen)
        self.load_panel = add_element(blur, load_panel,
                                      ((RESOLUTION[0] - load_panel.get_width()) / 2,
                                       (RESOLUTION[1] - load_panel.get_height()) / 2))

        self.mouse_handler = MouseEvents(self.screen, self.player, self.frame)

        self.chosen_obj = None
        self.chosen_door = None
        self.hovered_obj = None

        running = True
        while running:
            events = pygame.event.get()
            for event in events:

                mouse_pos = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    # self.transition.transition(pos=(self.player.visual_pos[0] + SCENES[SCENE_NAME]["cell"][0] / 2,
                    #             self.player.visual_pos[1] + SCENES[SCENE_NAME]["cell"][1] / 2),
                    #         transition_type='circle_in')
                    return None, None

                if self.chosen_door:
                    next_scene, next_grid_pos = self.toggle_panel(self.chosen_door, event)
                    if next_scene:
                        # self.transition.transition(pos=(next_grid_pos[0] * SCENES[next_scene]["cell"][0],
                        #                                 next_grid_pos[1] * SCENES[next_scene]["cell"][0]),
                        #                            transition_type="hole",
                        #                            next_scene=next_scene)
                        return next_scene, next_grid_pos

                if self.chosen_obj:
                    if not self.panel_fl:
                        if self.chosen_obj == "Load":
                            self.screen.blit(self.load_panel, (0, 0))
                        self.panel_fl = True
                    elif self.panel_fl and event.type == pygame.KEYDOWN:
                        next_scene, next_grid_pos = self.toggle_panel(self.chosen_obj, event)
                        if next_scene:
                            return next_scene, next_grid_pos
                    pygame.display.update()
                    continue

                self.mouse_handler.set_pos(mouse_pos)

                self.screenCopy, self.hovered_obj = self.mouse_handler.get_hover_frame(self.screenCopy,
                                                                                       self.hovered_obj)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.chosen_door, self.chosen_obj = self.mouse_handler.click()
                    events.append(pygame.event.Event(pygame.USEREVENT, {}))
                    continue

                if event.type == pygame.KEYDOWN:
                    pressed = event.key
                    player_response = self.player.handle_event(pressed)

                    if player_response == "Move":
                        pass
                    if player_response == "Interact":
                        self.chosen_obj = self.player.interacted_obj
                        if self.chosen_obj:
                            events.append(pygame.event.Event(pygame.USEREVENT, {}))
                            continue
                    if player_response == "Door":
                        self.chosen_door = SCENES[SCENE_NAME]['DOORS'][self.player.get_current_door()]

                    self.player.update(self.screenCopy)

    def toggle_panel(self, name, event):
        """
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:

            if name == "Menu":
                self.player.update(self.screen)
                self.transition.transition(transition_type='zelda_rl', next_scene=name)

                # Player re-init
                self.player.deactivate(active=True)
                self.player.re_init(name=self.player.name, scene="Menu")

                return name, (13, self.player.get_grid_pos()[1])

            if name == "Load":
                # Handle load scenes here
                return "Gameplay", (0, 0)

                # current_profile.json format
                # {
                #     "username": "a",
                #     "level": "Easy",
                #     "mode": "Manual",
                #     "score": 0,
                #     "maze": ""
                #     "player_pos": (-1, -1)
                #     "end_pos": (-1, -1)
                # }
                next_scene, next_grid_pos = self.load(event)
                if next_scene:
                    self.player.deactivate(active=True)
                    return next_scene, next_grid_pos

            if name == "Easy":
                print("Easy")
                self.set_current_mode("Easy")
                return "Gameplay", (0, 0)

            if name == "Medium":
                print("Medium")
                self.set_current_mode("Medium")
                return "Gameplay", (0, 0)

            if name == "Hard":
                print("Hard")
                self.set_current_mode("Hard")
                return "Gameplay", (0, 0)

        return None, None

    def set_current_mode(self, level):
        """
        Set the current mode of the game into the ```current_profile.json```
        """
        current_profile = {
            "player.name": self.player.name,
            "level": level,
            "mode": "Manual",
            "score": 0,
            "player.grid_pos": [-1, -1],
            "player.visual_pos": [-1, -1],
            "maze_toString": []
        }
        with open("current_profile.json", "w") as fi:
            json.dump(current_profile, fi, indent=4)

    def load(self, event):

        if event.type == pygame.KEYDOWN:
            # self.screen.blit(self.leaderboard_panel, (0, 0))
            if event.key == pygame.K_ESCAPE:
                self.panel_fl = False
                return "Play", self.player.get_grid_pos()  # [PROTOTYPE]

        pygame.display.update()
        return None, None
