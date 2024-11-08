import pygame
import numpy as np
from GridMapObject import GridMapObject


class GridMap:
    """
    This is a class to represent Grid Map Instance
    """

    def __init__(self, name, resolution, cell):
        self.name = name
        self.grid_map = np.full((resolution[1] // cell[1], resolution[0] // cell[0]), GridMapObject.FREE)

    def get_grid(self):  # Pass by reference
        return self.grid_map


class MapManager:
    """
    This is a class to manage Grid Map Instances
    """

    def __init__(self, **kwargs):
        # Create a grid path in order to move character
        self.list_maps = kwargs["list_maps"]
        self.map_grids = {}
        for item in self.list_maps:
            self.map_grids[item] = GridMap(name=item, resolution=kwargs["resolution"], cell=kwargs["cell"][item])
        self.init_preset()

    def init_preset(self):  # GridMap.py y, x -> LoginScreen.py x, y
        """
        Initialize preset grid map
        :return:
        """

        def loginScene():
            """
            Initialize Login Scene
            :return:
            """
            grid = self.map_grids["Login"].get_grid()

            # EXIT CAVE

            grid[:6, :] = [[GridMapObject.WALL]]
            grid[5, 12:15] = [GridMapObject.FREE]

            grid[5, 9] = GridMapObject.FREE
            grid[5, 17] = GridMapObject.FREE
            grid[4, 13] = GridMapObject.DOOR  # LoginScreen.py -> door_pos["Exit"]

            # LOG-IN HOUSE

            grid[6:11, :10] = [[GridMapObject.WALL]]
            grid[10, 4] = GridMapObject.FREE
            grid[9, 4] = GridMapObject.DOOR  # LoginScreen.py -> door_pos["Login"]

            # REGISTER HOUSE

            grid[6:11, 17:] = [[GridMapObject.WALL]]
            grid[10, 22] = GridMapObject.DOOR  # LoginScreen.py -> door_pos["Register"]

            # TREES

            grid[:, :3] = [[GridMapObject.WALL]]  # LEFT
            grid[:, -3:] = [[GridMapObject.WALL]]  # RIGHT

            # BEACH

            grid[-4, :] = [GridMapObject.WALL]

        def menuScene():
            """
            Initialize Menu Scene
            :return:
            """

            grid = self.map_grids["Menu"].get_grid()
            # DECORATES
            grid[:3, :4] = [[GridMapObject.WALL]]  # clock,etc
            grid[2, -6] = GridMapObject.WALL  # cloth hanger
            grid[4, 6:9] = [GridMapObject.WALL]  # TV
            grid[5:8, 4:11] = [[GridMapObject.WALL]]
            grid[7, 10] = GridMapObject.FREE

            # WALL
            grid[:2, :] = [[GridMapObject.WALL]]

            # MAIN DOOR
            grid[1, -4] = GridMapObject.DOOR

            grid[:, 0] = [GridMapObject.DOOR]
            grid[:, 14] = [GridMapObject.DOOR]

            pass

        def playScene():
            """
            Initialize Play Scene
            :return:
            """
            grid = self.map_grids["Play"].get_grid()

            grid[:2, :] = [[GridMapObject.WALL]]  # clock,etc
            grid[2, 4:] = [GridMapObject.WALL]
            grid[3, 13:15] = [GridMapObject.WALL]

            grid[:, 0] = [GridMapObject.DOOR]

            grid[5, 9:11] = [GridMapObject.DOOR]
            grid[7, 11:13] = [GridMapObject.DOOR]
            grid[9, 8:10] = [GridMapObject.DOOR]
            pass

        def leaderBoardScene():
            """
            Initialize Leaderboard Scene
            :return:
            """
            grid = self.map_grids["Leaderboard"].get_grid()

            # WALL
            grid[:3, :] = [[GridMapObject.WALL]]
            grid[:9, :2] = [[GridMapObject.WALL]]
            grid[4, 2] = GridMapObject.WALL
            grid[5:7, 6:9] = [[GridMapObject.WALL]]

            grid[:, 14] = [GridMapObject.DOOR]

            pass

        def settingsScene():
            """
            Initialize Settings Scene
            :return:
            """
            pass
        def win():

            pass
        loginScene()
        menuScene()
        playScene()
        leaderBoardScene()
        settingsScene()
        win()

    def get_map(self, name):
        """
        Get grid map by name
        :param name:
        :return:
        """

        return self.map_grids[name]
