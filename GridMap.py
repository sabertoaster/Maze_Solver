import pygame
import numpy as np
from GridMapObject import GridMapObject

class GridMap:
    def __init__(self, name, resolution, cell):
        self.name = name
        self.grid_map = np.full(
            (resolution[1] // cell[1], resolution[0] // cell[0]),
            GridMapObject.FREE)

    def get_grid(self):  # Pass by reference
        return self.grid_map


class MapManager:
    def __init__(self, **kwargs):
        # Create a grid path in order to move character
        self.list_maps = kwargs["list_maps"]
        self.map_grids = {}
        for item in self.list_maps:
            self.map_grids[item] = GridMap(name=item, resolution=kwargs["resolution"], cell=kwargs["cell"])
        self.init_preset()
        print(self.map_grids["Login"].get_grid())

    def init_preset(self):
        def loginScene():
            grid = self.map_grids["Login"].get_grid()

            # EXIT CAVE

            grid[:6, :] = [[GridMapObject.WALL]]
            grid[5, 12:15] = [GridMapObject.FREE]
            grid[4, 13] = GridMapObject.DOOR


            # LOG-IN HOUSE

            grid[6:11, :10] = [[GridMapObject.WALL]]
            grid[10, 4] = GridMapObject.FREE
            grid[9, 4] = GridMapObject.DOOR

            # REGISTER HOUSE

            grid[6:11, 17:] = [[GridMapObject.WALL]]
            grid[10, 22] = GridMapObject.DOOR

            # TREES

            grid[:, :3] = [[GridMapObject.WALL]] #LEFT
            grid[:, -3:] = [[GridMapObject.WALL]] #RIGHT

            # BEACH

            grid[-4, :] = [GridMapObject.WALL]

        def menuScene():
            pass

        def playScene():
            pass

        def leaderBoardScene():
            pass

        def settingsScene():
            pass

        loginScene()
        menuScene()
        playScene()
        leaderBoardScene()
        settingsScene()

    def get_map(self, name):
        return self.map_grids[name]
