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
        'BGM': "theme.mp3"
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
        'BGM': 'theme.mp3',
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
        'BGM': 'theme.mp3',
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
        'BGM': 'theme.mp3',
    },
    'Settings': {
        'BG': 'settings_BG.png',
        'OBJECTS_POS': {},
        'HOVER_FRAME': {},
        'cell': (80, 80),
        'initial_pos': (0, 0),   
        'BGM': 'theme.mp3',
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

        'OBJECTS_POS': {},

        'HOVER_FRAME': {},

        'cell': (80, 80),

        'initial_pos': (0, 0),
        'BGM': 'theme.mp3',
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
CELLS_LIST = {"Login": (40, 40), "Menu": (80, 80), "Play": (80, 80), "Leaderboard": (80, 80), "Settings": (80, 80)}
MAPS_LIST = ["Login", "Menu", "Play", "Leaderboard", "Settings"]

# MISCs
COLORS = {
    'WHITE': (200, 200, 200),
}

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
        'Login': 'theme.mp3',
        'Menu': 'theme.mp3',
        'Play': 'theme.mp3',
    },
    'SFX': {
        'move': 'move.mp3',
        'interact': 'interact.mp3',
    }
}

FONTS = {
    'default':  RESOURCE_PATH + 'fonts/PixeloidSans.ttf',
    'default_bold': RESOURCE_PATH + 'fonts/PixeloidSansBold.ttf',
}