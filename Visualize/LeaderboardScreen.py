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
from Visualize.Mouse_Events import Mouse_Events
from Visualize.Transition import Transition

FILENAME = "leaderboard_BG.png"

# [PROTOTYPE]
PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": (80, 80)  # 12 cells column, 8 cells row
}
# [PROTOTYPE]
WHITE = (200, 200, 200)


def drawGrid(screen):
    """
    FOR FUCKING DEBUG THE GRID MAP
    :param screen:
    :return:
    """
    blockSize = PARAMS["cell"][0]  # Set the size of the grid block
    for x in range(0, PARAMS["resolution"][0], blockSize):
        for y in range(0, PARAMS["resolution"][1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, WHITE, rect, 1)


# [PROTOTYPE]

class LeaderboardScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """

    def __init__(self, screen, res_cel, path_resources):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """
        self.resolution, self.cell = res_cel
        self.frame = morph_image(path_resources + FILENAME, self.resolution)
        self.pth_re = path_resources
        self.screen = screen
        self.door_pos = {
        }

        # Transition effect
        self.transition = Transition(self.screen, self.resolution)

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """
        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        drawGrid(screen=self.screen)

        self.player = player
        # print(self.player.grid_map.get_map(self.player.current_scene).get_grid()[12, 12])
        self.panel_fl = False  # CÁI NI Bị DOWN
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background
        self.blur = blur_screen(screen=self.screen.copy())

        # Start transition effect
        # self.transition.transition(pos=(self.player.visual_pos[0] + PARAMS["cell"][0] / 2,
        #                                 self.player.visual_pos[1] + PARAMS["cell"][1] / 2),
        #                            transition_type='circle_out')  # draw transition effect
        self.mouse_handler = Mouse_Events(self.screen, self.player, self.frame, PARAMS)

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    return None, None  # Fucking transmit signal to another scene here, this is just a prototype

    def toggle_panel(self, event, name):
        """
        :param event:
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:
            self.player.deactivate(active=False)
            # if name == "Menu":
            #     next_scene, next_grid_pos = self.login(event)
            #
            #     if next_scene:
            #         self.player.deactivate(active=True)
            #         return next_scene, next_grid_pos
            #
            # if name == "Gameplay":
            #     next_scene, next_grid_pos = self.register(event)
            #
            #     if next_scene:
            #         self.player.deactivate(active=True)
            #         return next_scene, next_grid_pos

        return None, None
