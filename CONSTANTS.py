from enum import Enum

# Game Window Constants
RESOLUTION = (1200, 800)
FPS = 60

# Path to Resources
RESOURCE_PATH = "Resources/"

# Scenes' Constants
SCENES = {
    'Login': {
        'BG': 'miniTown_BG.png',

        'DOORS': {
            (4, 9): "Login",
            (13, 4): "Exit",
            (22, 10): "Register"
        },

        'DOORS_CLICK_RANGE': {
            "Login" : [[x, y] for x in range(6, 10) for y in range(3, 9)],
            "Register" : [[x, y] for x in range(6, 11) for y in range(18, 27)],
            "Exit" : [[4,13]]
        },
        
        'OBJECTS_POS': {
            "Login" : [[x, y] for x in range(6, 10) for y in range(3, 9)],
            "Register" : [[x, y] for x in range(6, 11) for y in range(18, 27)],
            "Exit" : [[4,13]]    
        },

        'HOVER_FRAME': {
            "Login": "miniTown_BG_login_hover.png",
            "Register": "miniTown_BG_register_hover.png",
            "Exit": "miniTown_BG_exit_hover.png"
        },

        'cell': (40, 40),
        'initial_pos': (12, 12),
    },

    'Menu': {
        'BG': 'livingRoom_BG.png',

        'DOORS': {
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
        },
        
        'DOORS_CLICK_RANGE': {
            'Login': [[1,11]],
            'Leaderboard': [[x,0] for x in range(3, 10)],
            'Play': [[x,14] for x in range(2, 10)],
        },

        'OBJECTS_POS': {
            "Music_box": [[x,y] for x in range(1, 3) for y in range(2, 4)],
            "Credit": [[x,y] for x in range(4, 6) for y in range(6, 9)],
            "Skin": [[x,9] for x in range(0, 3)],
        },

        'HOVER_FRAME': {
            'Music_box': 'livingRoom_BG_music_box_hover.png',
            'Credit': 'livingRoom_BG_credit_hover.png',
            'Skin': 'livingRoom_BG_skin_hover.png',
        },

        'cell': (80, 80),

        'initial_pos': (11, 2),
    },

    'Play': {
        'BG': 'kitchen_BG.png',

        'DOORS': {
            (0, 2): "Menu",
            (0, 3): "Menu",
            (0, 4): "Menu",
            (0, 5): "Menu",
            (0, 6): "Menu",
            (0, 7): "Menu",
            (0, 8): "Menu",
            (0, 9): "Menu",
        },
        
        'DOORS_CLICK_RANGE': {
            'Menu': [[x,0] for x in range(2, 10)]
        },

        'OBJECTS_POS': {},

        'HOVER_FRAME': {},

        'cell': (80, 80),

        'initial_pos': (0, 0),
    },

    'Leaderboard': {
        'BG': 'leaderboard_BG.png',

        'DOORS': {
            (14, 2): "Menu",
            (14, 3): "Menu",
            (14, 4): "Menu",
            (14, 5): "Menu",
            (14, 6): "Menu",
            (14, 7): "Menu",
            (14, 8): "Menu",
            (14, 9): "Menu",
        },
        
        'DOORS_CLICK_RANGE': {
            'Menu': [[x,14] for x in range(2, 10)]
        },

        'OBJECTS_POS': {},

        'HOVER_FRAME': {},

        'cell': (80, 80),

        'initial_pos': (0, 0),
    },
    'Settings': {
        'BG': 'settings_BG.png',
        'OBJECTS_POS': {},
        'HOVER_FRAME': {},
        'cell': (80, 80),
        'initial_pos': (0, 0),   
        'BGM': 'town_bgm.mp3',
    },
}

# Skins
AVATAR = {
    "Tom": {"down": "tom_icon_d.png",
            "right": "tom_icon_r.png",
            "left": "tom_icon_l.png",
            "up": "tom_icon_u.png"},

    "orangeTom": {"down": "orangeTom_icon_d.png",
                  "right": "orangeTom_icon_r.png",
                  "left": "orangeTom_icon_l.png",
                  "up": "orangeTom_icon_u.png"},

    "blackTom": {"down": "blackTom_icon_d.png",
                 "right": "blackTom_icon_r.png",
                 "left": "blackTom_icon_l.png",
                 "up": "blackTom_icon_u.png"},
}

# Movement
MOVEMENT = {
            "left": (-1, 0),
            "right": (1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }

# Grid Map Object
CELLS_LIST = {"Login": (40, 40), "Menu": (80, 80), "Play": (80, 80), "Leaderboard": (80, 80), "Settings": (80, 80), "Gameplay": (20, 20)}
MAPS_LIST = ["Login", "Menu", "Play", "Leaderboard", "Settings", "Gameplay"]

# MISCs
class COLORS(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)
    GREY = (128, 128, 128)
    LIGHT_GREY = (211, 211, 211)
    DARK_GREY = (169, 169, 169)
    LIGHT_BLUE = (173, 216, 230)
    LIGHT_GREEN = (144, 238, 144)
    LIGHT_YELLOW = (255, 255, 224)
    LIGHT_ORANGE = (255, 160, 122)
    LIGHT_PURPLE = (221, 160, 221)
    LIGHT_PINK = (255, 182, 193)
    LIGHT_BROWN = (210, 105, 30)
    LIGHT_CYAN = (224, 255, 255)
    LIGHT_RED = (255, 99, 71)
    LIGHT_MAGENTA = (255, 182, 193)
    LIGHT_BLACK = (25, 25, 25)

print(type(COLORS.WHITE.value))

AVATAR = {
    "Tom": {"down": "tom_icon_d.png",
            "right": "tom_icon_r.png",
            "left": "tom_icon_l.png",
            "up": "tom_icon_u.png"},
    
    "orangeTom": {"down": "orangeTom_icon_d.png",
                  "right": "orangeTom_icon_r.png",
                  "left": "orangeTom_icon_l.png",
                  "up": "orangeTom_icon_u.png"},

    "blackTom": {"down": "blackTom_icon_d.png",
                 "right": "blackTom_icon_r.png",
                 "left": "blackTom_icon_l.png",
                 "up": "blackTom_icon_u.png"},
}

SOUNDS = {
    'BGM': {
        'Login': {
            'file_name': 'town_bgm.mp3',
            'volume': 0.5
        },
        'Menu': {
            'file_name': 'house_bgm.mp3',
            'volume': 0.5
        },
        'Play': {
            'file_name': 'house_bgm.mp3',
            'volume': 0.5
        },
    },
    'SFX': { 
        'bump': {
            'file_name': 'bump.mp3',
            'volume': 1.0
        },
        'interact': {
            'file_name': 'interact.mp3',
            'volume': 1.0
        },
        'circle_in': {
            'file_name': 'door_enter.mp3',
            'volume': 1.0
        },
        'circle_out': {
            'file_name': 'door_enter.mp3',
            'volume': 1.0
        },
    }
}

FONTS = {
    'default':  RESOURCE_PATH + 'fonts/PixeloidSans.ttf',
    'default_bold': RESOURCE_PATH + 'fonts/PixeloidSansBold.ttf',
}


# CURRENT PLAY MODE and LEVEL
class PLAY_MODE(Enum):
    MANUAL = 0
    AUTO = 1


class LEVEL(Enum):
    EASY = {"id": 0, "maze_size": (20, 20)}
    MEDIUM = {"id": 1, "maze_size": (40, 40)}
    HARD = {"id": 0, "maze_size": (100, 100)}


CURRENT_PLAY_MODE = PLAY_MODE.MANUAL
CURRENT_LEVEL = LEVEL.EASY

#CREDIT
CREDIT = {
    "MEMBERS": {
        "BU CAC": "KHOA NGUYEN (23122036)",
        "CAC": "LOZ AN (23122020)",
        "LOZ BENH": "HUY (23122008)",
        "MIEN TAY": "KIET (23122039)",
        "AN THIT LOLI": "HUY MINI (23122033)"
    },
    "TEACHERS": {
        "BEO": "MINHBEO",
        "CUU EM THAY OI": "TUNGLE"
    }
}

