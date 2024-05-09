PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": {"Login": (40, 40), "Menu": (80, 80), "Play": (80, 80), "Leaderboard": (80, 80), "Settings": (80, 80)}, # 12 cells column, 8 cells row
    "scenes": ["Login", "Menu", "Play", "Leaderboard", "Settings"],
    "initial_pos": {"Login": (12, 12), "Menu": (11, 2), "Play": (0, 0), "Leaderboard": (0, 0), "Settings": (0, 0)}  # need adjusting
}

SCENES = {
    'Login': {
        'ORIGINAL_FRAME': 'miniTown_BG.png',
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
        'ORIGINAL_FRAME': 'livingRoom_BG.png',
        'OBJECTS_POS': {
            "Login" : [[11, 1]],
        },
        'HOVER_FRAME': {
        },
        'cell': (80, 80),
        'initial_pos': (11, 2),
    },
    'Leaderboard': {
        'ORIGINAL_FRAME': 'leaderboard_BG.png',
        'OBJECTS_POS': {},
        'HOVER_FRAME': {},
        'cell': (80, 80),
        'initial_pos': (0, 0),
    },
    'Settings': {},
}

FPS = 60

COLORS = {
    'WHITE': (200, 200, 200),
}

BG = {
    "Login": "login_BG.png",
    "Menu": "livingRoom_BG.png",
    "Play": "kitchen_BG.png",
    "Leaderboard": "leaderboard_BG.png",
    "Settings": "settings_BG.png"
}