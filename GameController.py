from Visualize import basic     # [PROTOTYPE]
from Algorithms import basicAlgo    # [PROTOTYPE]
from Algorithms import MazeGeneration


class GameController:
    def __init__(self):
        self.visualizer = basic.Visualizer("Visualize/Resources/") # [PROTOTYPE]

    def run(self):
        self.visualizer.loading() # [PROTOTYPE]
