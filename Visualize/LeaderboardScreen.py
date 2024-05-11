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

PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": (80, 80)  # 12 cells column, 8 cells row
}

SCENE_NAME = "Leaderboard"


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
            pygame.draw.rect(screen, COLORS['WHITE'], rect, 1)


# [PROTOTYPE]

class LeaderboardScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """
    def __init__(self, screen):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """

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

        # Draw Player
        self.player = player
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        
        # Play BGM

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    return None, None
                if event.type == pygame.KEYDOWN:
                    pressed = event.key
                    player_response = self.player.handle_event(pressed)
                    if player_response == "Move":
                        pass
                    if player_response == "Interact":
                        pass  # Handle Interact Here
                    if player_response == "Door":
                        self.player.update(self.screenCopy)
                        self.panel_fl = True
                        self.chosen_door = SCENES[SCENE_NAME]['DOORS'][self.player.get_current_door()]
                        next_scene, next_grid_pos = self.toggle_panel(self.chosen_door)
                        if next_scene:
                            player_response = self.player.handle_event(pressed)
                            return next_scene, next_grid_pos


                    # if self.player.handle_event(pressed):  # Handle interact from player
                    #     pass
                    # if self.player.get_grid_pos() in DOOR_POS[SCENE_NAME]:
                    #     pass
                    self.player.update(self.screenCopy)

    def toggle_panel(self, name):
        """
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:
            if name == "Menu":
                self.player.update(self.screen)
                self.transition.transition(transition_type='zelda_lr', next_scene=name)
                return name, (1, self.player.get_grid_pos()[1])
        return None, None
