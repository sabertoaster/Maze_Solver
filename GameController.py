# Custom imports
import sys

from Visualize.Visualizer import Visualizer  # [PROTOTYPE]
from Algorithms import basicAlgo  # [PROTOTYPE]
from Algorithms import MazeGeneration

# Pre-defined imports
import pygame
import numpy as np
import cv2

# init hyperparameters here
PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),
    "cell": (8, 8)
}
FPS = 60

class GameController:
    def __init__(self):
        self.visualizer = Visualizer(PARAMS["resources"], PARAMS["resolution"])  # [PROTOTYPE]
        self.clock = pygame.time.Clock()  # Define a variable to control the main loop


    def run(self):
        self.game_state_manager = GameStateManager("Login") # [PROTOTYPE]
        self.visualizer.start_visualize()  # [PROTOTYPE]
        # [MAIN GAME LOOP]
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.exit()
                    sys.exit()
            self.visualizer.draw_scene(self.game_state_manager.get_state())
            pygame.display.update()
            self.clock.tick(FPS)
        # [MAIN GAME LOOP]


class GameStateManager:
    def __init__(self, current_state: str):
        self.game_state = current_state

    def change_state(self, new_state: str):
        self.game_state = new_state

    def get_state(self) -> str:
        return self.game_state