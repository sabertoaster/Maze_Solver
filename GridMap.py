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

            # LOG-IN HOUSE

            grid[:5, 2:9] = [[GridMapObject.WALL] * 7] * 5
            grid[5:7, 2:6] = [[GridMapObject.WALL] * 4] * 2
            grid[5:7, 7:9] = [[GridMapObject.WALL] * 2] * 2
            grid[5, 6] = GridMapObject.DOOR

            # REGISTER HOUSE

            grid[1:6, -8:-1] = [[GridMapObject.WALL] * 7] * 5
            grid[6, -7:-2] = [[GridMapObject.WALL] * 5]
            grid[6, -5] = GridMapObject.DOOR

            # DECORATES
            grid[2, 2] = GridMapObject.DOOR
            grid[:3, -5:] = [[GridMapObject.WALL] * 5] * 3
            grid[2, -3:-1] = [GridMapObject.DOOR] * 2

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
