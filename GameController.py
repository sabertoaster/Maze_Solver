# Custom imports
from Player import Player
from Visualize.Visualizer import Visualizer  # [PROTOTYPE]
from GridMap import MapManager
from Sounds import SoundsHandler
from Save import *
from Visualize.Playgif import play_gif

# Pre-defined imports
import sys
import pygame
import numpy as np
import cv2
from enum import Enum

# init hyperparameters here
from CONSTANTS import FPS, RESOLUTION, CELLS_LIST, MAPS_LIST, SCENES, SOUNDS


class GameController:
    """
    This is a class to represent Game Controller Instance
    """

    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(200, 125)
        initial_scene = "Login"
        self.game_state_manager = GameStateManager(initial_scene)  # [PROTOTYPE]
        self.clock = pygame.time.Clock()  # Define a variable to control the main loop
        self.screen = pygame.display.set_mode(
            RESOLUTION)  # Create a surface on screen that has the size of `resolution`

        # INSTANTIATE SCREEN GRID MAP
        self.grid_map = MapManager(resolution=RESOLUTION,
                                   cell=CELLS_LIST,
                                   list_maps=MAPS_LIST)  # [PROTOTYPE]

        # INSTANTIATE SOUNDS HANDLER
        self.sounds_handler = SoundsHandler()
        self.sounds_handler.turn_on()
        for key, val in SOUNDS['SFX'].items():
            self.sounds_handler.add_sfx(key, val['file_name'])

        # INSTANTIATE PLAYER
        self.player = Player(self.screen,
                             grid_map=self.grid_map,
                             current_scene=initial_scene,
                             initial_pos=SCENES[initial_scene]["initial_pos"],
                             sounds_handler=self.sounds_handler)  # [PROTOTYPE]

        # INSTANTIATE VISUALIZER
        self.visualizer = Visualizer(self.screen,
                                     self.player,
                                     sounds_handler=self.sounds_handler)  # [PROTOTYPE]

        # INSTANTIATE ALGORITHMS
        # pass

        # INSTANTIATE MAZE
        # pass

    def run(self):
        self.visualizer.start_visualize()  # [PROTOTYPE]
        # [MAIN GAME LOOP]
        pygame.init()

        # play_gif(self.screen) # [PROTOTYPE]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.exit()
                    sys.exit(0)
            next_scene, next_grid_pos = self.visualizer.draw_scene(self.game_state_manager.get_state())
            # Fucking transmit signal to another scene here, this is just a prototype
            if next_scene:
                self.game_state_manager.change_state(next_scene)

                self.player.set_current_scene(next_scene, initial_pos=next_grid_pos)
            else:
                running = False
            # pygame.display.update()
            self.clock.tick(FPS)
        # [MAIN GAME LOOP]


class GameStateManager:
    def __init__(self, current_state: str):
        self.game_state = current_state

    def change_state(self, new_state: str):
        self.game_state = new_state

    def get_state(self) -> str:
        return self.game_state
