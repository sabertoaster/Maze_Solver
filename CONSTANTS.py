# Game Window Constants
RESOLUTION = (1200, 800)
FPS = 60

# Path to Resources
RESOURCE_PATH = "Visualize/Resources/"

# Scenes' Constants
SCENES = {
    'Login': {
        'BG': 'miniTown_BG.png',

        'DOORS': {
            (4, 9): "Login",
            (13, 4): "Exit",
            (22, 10): "Register"
        },

        'OBJECTS_POS': {
            "Login": [[x, y] for x in range(6, 10) for y in range(3, 9)],
            "Register": [[x, y] for x in range(6, 11) for y in range(18, 27)],
            "Exit": [[4, 13]]
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

        'OBJECTS_POS': {
            "Login": [[11, 1]],
        },

        'HOVER_FRAME': {
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

        'OBJECTS_POS': {},

        'HOVER_FRAME': {},

        'cell': (80, 80),

        'initial_pos': (0, 0),
    },
    'Settings': {},
}
PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": {"Login": (40, 40), "Menu": (80, 80), "Play": (80, 80), "Leaderboard": (80, 80), "Settings": (80, 80)},
    # 12 cells column, 8 cells row
    "scenes": ["Login", "Menu", "Play", "Leaderboard", "Settings", "Gameplay"],
    "initial_pos": {"Login": (12, 12), "Menu": (11, 2), "Play": (0, 0), "Leaderboard": (0, 0), "Settings": (0, 0),
                    "Gameplay": (0, 0)}  # need adjusting
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
