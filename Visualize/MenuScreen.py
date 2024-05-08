import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element
from Visualize.Transition import Transition

FILENAME = "livingRoom_BG.png"

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
        self.frame = morph_image(path_resources + FILENAME, self.resolution)
        self.pth_re = path_resources
        self.screen = screen
        tup = (14, slice(0, 14))

        self.door_pos = {
            (11, 1): "Login",

            (0, 3): "Leaderboard",
            (0, 4): "Leaderboard",
            (0, 5): "Leaderboard",
            (0, 6): "Leaderboard",
            (0, 7): "Leaderboard",
            (0, 8): "Leaderboard",
            (0, 9): "Leaderboard",

            (14, 2): "Play",
            (14, 3): "Play",
            (14, 4): "Play",
            (14, 5): "Play",
            (14, 6): "Play",
            (14, 7): "Play",
            (14, 8): "Play",
            (14, 9): "Play",
        }
        self.transition = Transition(self.screen, self.resolution)


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
                        self.chosen_door = self.door_pos[self.player.get_current_door()]
                        next_scene, next_grid_pos = self.toggle_panel(self.chosen_door)
                        if next_scene:
                            player_response = self.player.handle_event(pressed)
                            return next_scene, next_grid_pos


                    # if self.player.handle_event(pressed):  # Handle interact from player
                    #     pass
                    # if self.player.get_grid_pos() in self.door_pos:
                    #     pass
                    self.player.update(self.screenCopy)

    def toggle_panel(self, name):
        """
        :param name: to know whether if the player step into which door
        :return:
        """
        self.transition.transition(pos=(self.player.visual_pos[0] + PARAMS["cell"][0] / 2,
                                        self.player.visual_pos[1] + PARAMS["cell"][1] / 2),
                                   transition_type='circle_in')
        if name:
            if name == "Login":
                print(name, self.player.params["initial_pos"][name])
                return name, self.player.params["initial_pos"][name]

            if name == "Leaderboard":
                print(self.player.get_grid_pos())
                return name, (13, self.player.get_grid_pos()[1])

            if name == "Play":
                return name, (1, self.player.get_grid_pos()[1])

        return None, None
