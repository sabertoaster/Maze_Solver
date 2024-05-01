from enum import Enum


# Enum class for Walls, Interactable Objects, Door, Free Space
class GridMapObject(Enum):
    """
    This is a class to represent Grid Map Object Enum
    """
    FREE = 0
    WALL = 1
    DOOR = 2
    INTERACTABLE = 3
    PLAYER = 4