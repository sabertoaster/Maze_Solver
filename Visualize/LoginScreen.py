import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
from Visualize.morph_image import morph_image
from Visualize.morph_image import add_element
from Visualize.morph_image import blur_screen

FILENAME = "miniTown_BG.png"

# [PROTOTYPE]
PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": (40, 40)  # 12 cells column, 8 cells row
}

OBJECTS = {
    "Login" : [[x, y] for x in range(6, 10) for y in range(3, 9)],
    "Register" : [[x, y] for x in range(6, 11) for y in range(18, 27)],
    "Exit" : [[4,13]]
}

OBJECTS_POS_RES = {
    "Login" : ((103, 227), (260,210)),
    "Register" : (10, 22),
    "Exit" : (13, 4)
}
# [PROTOTYPE]
WHITE = (200, 200, 200)


def drawGrid(screen):
    """
    FOR FUCKING DEBUG THE GRID MAP
    :param screen:
    :return:
    """
    blockSize = PARAMS["cell"][0]  # Set the size of the grid block
    for x in range(0, PARAMS["resolution"][0], blockSize):
        for y in range(0, PARAMS["resolution"][1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, WHITE, rect, 1)


# [PROTOTYPE]

class LoginScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """

    def __init__(self, screen, res_cel, path_resources):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """
        self.resolution, self.cell = res_cel
        self.frame = morph_image(path_resources + FILENAME, self.resolution)
        self.pth_re = path_resources
        print(self.pth_re)
        self.screen = screen
        self.door_pos = {
            (4, 9): "Login",
            (13, 4): "Exit",
            (22, 10): "Register"
        }

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """

        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        # drawGrid(screen=self.screen)

        self.player = player
        self.panel_fl = True  # CÁI NI Bị DOWN
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background
        self.blur = blur_screen(screen=self.screen.copy())

        ratio = 0.6
        panel_shape = self.resolution[0] * ratio, self.resolution[1] * ratio
        login_panel = morph_image(self.pth_re + "login_box.png", panel_shape)
        self.login_panel = add_element(self.blur, login_panel, (
            (self.resolution[0] - panel_shape[0]) / 2, (self.resolution[1] - panel_shape[1]) / 2))
        self.create_font()  # Create font for text input


        # a class to handle objects
        class House:
            def __init__(self, name, on_hover=False):
                self.pth_re = "Visualize/Resources/"
                self.name = name
                if on_hover:
                    self.box = morph_image(self.pth_re + self.name + "_hover.png", OBJECTS_POS_RES[self.name][1])
                else:
                    self.box = morph_image(self.pth_re + self.name + "_unhover.png", OBJECTS_POS_RES[self.name][1])
                self.pos = OBJECTS_POS_RES[self.name][0]

            def get_box(self):
                return self.box
                                

        self.running = True
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # pygame.quit()
                    return False  # Fucking transmit signal to another scene here, this is just a prototype
                
                if event.type == pygame.KEYDOWN:
                    pressed = event.key
                    if self.player.handle_event(pressed):  # Handle interact from player
                        pass
                    if self.player.get_grid_pos() in self.door_pos:
                        self.textinput_custom.update(events)
                        self.toggle_panel(event, self.door_pos[self.player.get_grid_pos()])
                        continue
                    self.player.update(
                        self.screenCopy)  # NEED TO OPTIMIZED, https://stackoverflow.com/questions/61399822/how-to-move-character-in-pygame-without-filling-background
                
                # handle click event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(pos)
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos() 
                        x, y = (pos[1] // PARAMS["cell"][0]), (pos[0] // PARAMS["cell"][1])
                        for key in OBJECTS.keys():
                            if [x,y] in OBJECTS[key]:
                                self.toggle_panel(event, key)
                                break
                        self.player.update(self.screenCopy)            


            # check if mouse is on object
            pos = pygame.mouse.get_pos() 
            x, y = (pos[1] // PARAMS["cell"][0]), (pos[0] // PARAMS["cell"][1])

            cur_obj = None
            for key in OBJECTS.keys():
                if [x,y] in OBJECTS[key]:
                    cur_obj = key
                    break   

            if cur_obj:
                house = House(cur_obj, on_hover=True)
                house_box = house.get_box()
                self.screen.blit(house_box, (house.pos[0], house.pos[1]))
                pygame.display.flip()
            else:
                for key in ["Login"]: #OBJECTS.keys(): fix later
                    house = House(key, on_hover=False)
                    house_box = house.get_box()
                    self.screen.blit(house_box, (house.pos[0], house.pos[1]))
                    pygame.display.flip()
                


            # self.screen.blit(self.frame, (0, 0))
            # pygame.display.flip()
            # for key, val in kwargs:
            #     screen.blit(val, (0, 0))
            #     pygame.display.flip()
            #     self.clock.tick(900)

    def toggle_panel(self, event, name):
        """
        :param event:
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:
            self.player.deactivate(active=False)

            if name == "Login":
                username, pwd = self.login()
            if name == "Exit":
                # Play outro animation here
                pygame.quit()
                exit()
            if name == "Register":
                pass

    def login(self):
        """
        Login panel
        """
        if self.panel_fl == True:
            self.textinput_custom.value = ""  # SUSSY FIRST TIME REMOVE CHARACTER FROM TEXT TO FUCKING AVOID INCONVENIENCE
            self.panel_fl = False

        panel_shape = self.resolution[0] * 0.9, self.resolution[1] * 0.6
        login_panel = morph_image(self.pth_re + "login_box.png", panel_shape)
        self.player.update(self.login_panel)
        self.screen.blit(self.textinput_custom.surface, (self.resolution[0] // 2, self.resolution[1] // 2 + 20))

        pygame.display.flip()
        # self.player.update(self.screen.copy())
        # self.login_panel = self.screen.copy()
        print(self.textinput_custom.value)
        return "username", "password"

    def register(self):
        """
        Register panel
        :return: username and password
        """
        pass

    def create_font(self):
        # But more customization possible: Pass your own font object
        font = pygame.font.Font(self.pth_re + "Fonts/PixeloidSans.ttf", 23)
        # Create own manager with custom input validator
        manager = TextInputManager(validator=lambda input: len(input) <= 10)
        # Pass these to constructor
        textinput_custom = TextInputVisualizer(manager=manager, font_object=font)

        # Customize much more
        textinput_custom.cursor_width = 4
        textinput_custom.cursor_blink_interval = 400  # blinking interval in ms
        textinput_custom.antialias = False
        textinput_custom.font_color = (0, 85, 170)
        self.textinput_custom = textinput_custom
