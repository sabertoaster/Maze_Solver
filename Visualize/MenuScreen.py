import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element

from CONSTANTS import PARAMS, COLORS, SCENES

SCENE_NAME = "Menu"

def drawGrid(screen):
    """
    FOR FUCKING DEBUG THE GRID MAP
    :param screen:
    :return:
    """
    blockSize = PARAMS["cell"][SCENE_NAME][0]  # Set the size of the grid block
    for x in range(0, PARAMS["resolution"][0], blockSize):
        for y in range(0, PARAMS["resolution"][1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, COLORS['WHITE'], rect, 1)


# [PROTOTYPE]

class MenuScreen:
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
        self.frame = morph_image(path_resources + SCENES[SCENE_NAME]['ORIGINAL_FRAME'], self.resolution)
        self.pth_re = path_resources
        self.screen = screen
        self.door_pos = {
            (11, 1): "Login"
        }

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """

        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        pygame.display.flip()
        drawGrid(screen=self.screen)

        self.player = player
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background
        self.blur = blur_screen(screen=self.screen.copy())

        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    # pygame.quit()
                    return None, None  # Fucking transmit signal to another scene here, this is just a prototype
                if event.type == pygame.KEYDOWN:
                    pressed = event.key
                    player_response = self.player.handle_event(pressed)

                    if player_response == "Move":
                        pass
                    if player_response == "Interact":
                        pass  # Handle Interact Here
                    if player_response == "Door":
                        next_scene, next_grid_pos = self.toggle_panel(event,
                                                                      self.door_pos[self.player.get_current_door()])
                        if next_scene:
                            return next_scene, next_grid_pos
                    # if self.player.handle_event(pressed):  # Handle interact from player
                    #     pass
                    # if self.player.get_grid_pos() in self.door_pos:
                    #     pass
                    self.player.update(
                        self.screenCopy)  # NEED TO OPTIMIZED, https://stackoverflow.com/questions/61399822/how-to-move-character-in-pygame-without-filling-background

    def toggle_panel(self, event, name):
        """
        :param event:
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:
            self.player.deactivate(active=False)

            if name == "Login":
                print(name, self.player.params["initial_pos"][name])
                self.player.deactivate(active=True)
                return name, self.player.get_GridMapObject_Player("Login")
            if name == "Exit":
                # Play outro animation here
                pygame.quit()
                exit()
            if name == "Register":
                self.register(event)
                pass
        return None, None
