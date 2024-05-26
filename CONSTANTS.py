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
            "Login": [[x, y] for x in range(6, 10) for y in range(3, 9)],
            "Register": [[x, y] for x in range(6, 11) for y in range(18, 27)],
            "Exit": [[4, 13]]
        },

        'OBJECTS_POS': {
            "Login": [[x, y] for x in range(6, 10) for y in range(3, 9)],
            "Register": [[x, y] for x in range(6, 11) for y in range(18, 27)],
            "Exit": [[4, 13]]
        },

        'OBJECTS_INTERACT_RANGE': {

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

        'BG_instructions': 'livingRoom_BG_instructions.png',

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
            'Login': [[1, 11]],
            'Leaderboard': [[x, 0] for x in range(3, 10)],
            'Play': [[x, 14] for x in range(2, 10)],
        },

        'OBJECTS_POS': {
            'Login': [[1, 11]],
            "Music_box": [[x, y] for x in range(1, 3) for y in range(2, 4)],
            "Credit": [[x, y] for x in range(4, 6) for y in range(6, 9)],
            "Skin": [[x, 9] for x in range(0, 3)],
        },

        'OBJECTS_INTERACT_RANGE': {
            'Credit': [(6, 3), (7, 3), (8, 3), (5, 4), (9, 4)],
            'Music_box': [(2, 3), (3, 3), (4, 2)],
            'Skin': [(10, 2), (8, 2), (9, 3)],
        },

        'HOVER_FRAME': {
            'Login': 'livingRoom_BG_exit_hover.png',
            'Music_box': 'livingRoom_BG_music_box_hover.png',
            'Credit': 'livingRoom_BG_credit_hover.png',
            'Skin': 'livingRoom_BG_skin_hover.png',
        },

        'cell': (80, 80),

        'initial_pos': (11, 2),
    },

    'Play': {
        'BG': 'kitchen_BG.png',
        
        'BG_instructions': 'kitchen_BG_instructions.png',

        'DOORS': {
            (0, 2): "Menu",
            (0, 3): "Menu",
            (0, 4): "Menu",
            (0, 5): "Menu",
            (0, 6): "Menu",
            (0, 7): "Menu",
            (0, 8): "Menu",
            (0, 9): "Menu",

            (9, 5): "Easy",
            (10, 5): "Easy",

            (11, 7): "Medium",
            (12, 7): "Medium",

            (8, 9): "Hard",
            (9, 9): "Hard",
        },

        'DOORS_CLICK_RANGE': {
            'Menu': [[x, 0] for x in range(2, 10)],
            'Easy': [[5, y] for y in range(9, 11)],
            'Medium': [[7, y] for y in range(11, 13)],
            'Hard': [[9, y] for y in range(8, 10)],
            # 'Load': [[x, y] for x in range(3) for y in range(4, 6)],
        },

        'OBJECTS_POS': {
            'Easy': [[5, y] for y in range(9, 11)],
            'Medium': [[7, y] for y in range(11, 13)],
            'Hard': [[9, y] for y in range(8, 10)],
            'Load': [[x, y] for x in range(3) for y in range(4, 6)],
        },

        'OBJECTS_INTERACT_RANGE': {
            'Load': [(3, 2), (4, 3), (5, 3)]
        },

        'HOVER_FRAME': {
            'Easy': 'kitchen_BG_easy_hover.png',
            'Medium': 'kitchen_BG_medium_hover.png',
            'Hard': 'kitchen_BG_hard_hover.png',
            'Load': 'kitchen_BG_fridge_hover.png',
        },

        'cell': (80, 80),

        'initial_pos': (0, 0),
    },

    'Leaderboard': {
        'BG': 'leaderboard_BG.png',

        'BG_instructions': 'leaderboard_BG_instructions.png',

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
            'Menu': [[x, 14] for x in range(2, 10)]
        },

        'OBJECTS_POS': {
            "Trophy": [[x, y] for x in range(5, 7) for y in range(6, 9)],
        },
        'OBJECTS_INTERACT_RANGE': {
            'Trophy': [(y, x) for x in range(4, 8) for y in range(5, 10)]
        },

        'HOVER_FRAME': {
            "Trophy": 'leaderboard_BG_trophy_hover.png',
        },

        'cell': (80, 80),

        'initial_pos': (0, 0),
    },
    'Settings': {
        'BG': 'settings_BG.png',
        'DOORS': {},
        'DOORS_CLICK_RANGE': {},
        'OBJECTS_POS': {},
        'OBJECTS_INTERACT_RANGE': {},
        'HOVER_FRAME': {},
        'cell': (80, 80),
        'initial_pos': (0, 0),
        'BGM': 'town_bgm.mp3',
    },
    "Gameplay": {
        'BG': '',
        'DOORS': {},
        'DOORS_CLICK_RANGE': {},
        'OBJECTS_POS': {},
        'OBJECTS_INTERACT_RANGE': {},
        'HOVER_FRAME': {},
        "initial_pos": (0, 0),
        "cell": (40, 40),
        "BGM": "gameplay.png",
    },
    "Win": {
        'BG': '',
        'DOORS': {},
        'DOORS_CLICK_RANGE': {},
        'OBJECTS_POS': {
            'yes': [(x, y) for x in range(11, 13) for y in range(8, 13)], 
            'no': [(x, y) for x in range(11, 13) for y in range(16, 21)],
        },
        'OBJECTS_INTERACT_RANGE': {    
        },
        'HOVER_FRAME': {
            'yes': 'continue_hover_yes.png',
            'no': 'continue_hover_no.png',    
        },
        "initial_pos": (0, 0),
        "cell": (40, 40),
        "BGM": "win.mp3",
    }
    # "full_variables_of_a_scene": {
    #     'BG': '',
    #     'BG_instructions': '',
    #     'DOORS': {},
    #     'DOORS_CLICK_RANGE': {},
    #     'OBJECTS_POS': {},
    #     'OBJECTS_INTERACT_RANGE': {},
    #     'HOVER_FRAME': {},
    #     'cell': (),
    #     'initial_pos': (),
    #     'BGM': '',
    # }
}

PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": {"Login": (40, 40), "Menu": (80, 80), "Play": (80, 80), "Leaderboard": (80, 80), "Settings": (80, 80),
             "Win": (80, 80)},
    # 12 cells column, 8 cells row
    "scenes": ["Login", "Menu", "Play", "Leaderboard", "Settings", "Gameplay", "Win"],
    "initial_pos": {"Login": (12, 12), "Menu": (11, 2), "Play": (0, 0), "Leaderboard": (0, 0), "Settings": (0, 0),
                    "Gameplay": (0, 0), "Win": (0, 0), }  # need adjusting
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
CELLS_LIST = {"Login": (40, 40), "Menu": (80, 80), "Play": (80, 80), "Leaderboard": (80, 80), "Settings": (80, 80),
              "Gameplay": (1, 1), "Win": (1, 1)}
MAPS_LIST = ["Login", "Menu", "Play", "Leaderboard", "Settings", "Gameplay", "Win"]


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
        'Credit': {
            'file_name': 'credit.mp3',
            'volume': 0.5
        },
        'Gameplay': {
            'file_name': 'gameplay.mp3',
            'volume': 0.5
        },
        'Win': {
            'file_name': 'win.mp3',
            'volume': 0.5
        },
        'Chasing': {
            'file_name': 'chasing.mp3',
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
        'door_open': {
            'file_name': 'door_enter.mp3',
            'volume': 1.0
        },
        'circle': {
            'file_name': 'circle.mp3',
            'volume': 1.0
        },
        'zelda': {
            'file_name': 'door_enter.mp3',
            'volume': 1.0
        },
        'falling': {
            'file_name': 'falling_down.mp3',
            'volume': 1.0
        },
        'landing': {
            'file_name': 'landing.mp3',
            'volume': 1.0
        },
    }
}

FONTS = {
    'default': RESOURCE_PATH + 'fonts/PixeloidSans.ttf',
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

# CREDIT
CREDIT = {
    "ABOUT US": {
        "": ['GROUP OF 5', 'FRESHMEN', 'HCMUS', 'K23'],
        "MEMBERS": ["Mai Duc Minh Huy (23122008)",
                    "Nguyen Thien An (23122020)",
                    "Le Hoang Minh Huy (23122033)",
                    "Nguyen Ngoc Khoa (23122036)",
                    "Huynh Trung Kiet (23122039)"],
    },
    "ROLES": {
        "Project Manager": "Mai Duc Minh Huy",
        "Lead Game Designer": "Nguyen Thien An",
        "Programmer": ["Le Hoang Minh Huy", "Nguyen Ngoc Khoa"],
        "Algorithm Specialist": "Huynh Trung Kiet",

        "Audio Specialist": "Nguyen Ngoc Khoa",
        "Art and Animation Specialist": "Nguyen Thien An",
    },
    "TOOLS USED": {
        "": ['PyCharm', 'Visual Studio Code', 'Git', 'GitHub', 'GIMP']
    },
    "ACKNOWLEDGEMENTS": {
        # "We would like to express our gratitude to our instructor, Nguyen Tran Duy Minh, for his guidance and support throughout the project.": "",
        "": ["All the assets used in the game are for educational purposes only.",
             "We do not own any of the assets used in the game."],
    },

    "SPECIAL THANKS TO": {
        "Nguyen Tran Duy Minh and Le Thanh Tung": "For guidance and support throughout the project.",
        # "Chan Nguyen": "For the inspiration and motivation to complete the project.",
        "HCMUS": "For providing the opportunity to learn and grow.",
        "You": "For playing our game.",
    },

    "THANKS FOR PLAYING": {

    }
}


# circular linked list
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class CircularLinkedList():
    def __init__(self, data):
        self.head = Node(None)
        if type(data) == list:
            for i in range(len(data)):
                self.push(data[i])
        elif type(data) == dict:
            for key in data.keys():
                self.push(key)
        else:
            self.push(data)

    def push(self, data):
        if self.head.data == None:
            self.head.data = data
            self.head.next = self.head
        else:
            new_node = Node(data)
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def pop(self):
        return_node = self.head
        self.head = self.head.next
        return return_node.data

    def back(self):
        temp = self.head
        while temp.next.next != self.head:
            temp = temp.next
        self.head = temp.next
        return temp.data

FIRST_SCENE = True