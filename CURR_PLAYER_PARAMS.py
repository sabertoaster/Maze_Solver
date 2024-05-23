# CURRENT PLAY MODE and LEVEL
from enum import Enum
class PLAY_MODE(Enum):#Enum
    MANUAL = 0
    AUTO = 1


class LEVEL(Enum):#
    EASY = {"id": 0, "maze_size": (20, 20)}
    MEDIUM = {"id": 1, "maze_size": (40, 40)}
    HARD = {"id": 0, "maze_size": (100, 100)}


CURRENT_PLAY_MODE = PLAY_MODE.MANUAL
CURRENT_LEVEL = LEVEL.EASY