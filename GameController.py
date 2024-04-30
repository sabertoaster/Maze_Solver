# Custom imports
from Player import Player
from Visualize.Visualizer import Visualizer  # [PROTOTYPE]
from GridMap import MapManager
from Algorithms import basicAlgo  # [PROTOTYPE]
from Algorithms import MazeGeneration

# Pre-defined imports
import sys
import pygame
import numpy as np
import cv2
from enum import Enum

# init hyperparameters here
PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": (40, 40),  # 12 cells column, 8 cells row
    "scenes": ["Welcome", "Login", "Menu", "Play", "Leaderboard", "Settings"]
}
FPS = 60


class GameController:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(200, 125)
        initial_scene = "Login"
        self.game_state_manager = GameStateManager(initial_scene)  # [PROTOTYPE]
        self.clock = pygame.time.Clock()  # Define a variable to control the main loop
        self.screen = pygame.display.set_mode(
            PARAMS["resolution"])  # Create a surface on screen that has the size of `resolution`

        # INSTANTIATE SCREEN GRID MAP
        self.grid_map = MapManager(resolution=PARAMS["resolution"], cell=PARAMS["cell"],
                                   list_maps=PARAMS["scenes"])  # [PROTOTYPE]

        # INSTANTIATE PLAYER
        self.player = Player(self.screen, (PARAMS["resolution"], PARAMS["cell"]), grid_map=self.grid_map, current_scene=initial_scene)  # [PROTOTYPE]

        # INSTANTIATE VISUALIZER
        self.visualizer = Visualizer(PARAMS, self.screen, self.player)  # [PROTOTYPE]

        # INSTANTIATE ALGORITHMS
        # pass

        # INSTANTIATE MAZE
        # pass

    def run(self):
        self.visualizer.start_visualize()  # [PROTOTYPE]
        # [MAIN GAME LOOP]
        pygame.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.exit()
                    sys.exit(0)
            running = self.visualizer.draw_scene(
                self.game_state_manager.get_state())  # Fucking transmit signal to another scene here, this is just a prototype
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
