import json
import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
import keyboard
import time
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element
from Visualize.TextBox import TextBox, FormManager, Color
from Visualize.Transition import Transition

FILENAME = "miniTown_BG.png"

# [PROTOTYPE]
PARAMS = {
    "resources": "Visualize/Resources/",
    "resolution": (1200, 800),  # ratio 3:2
    "cell": (40, 40)  # 12 cells column, 8 cells row
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

        # Tạo textbox nhập username/password
        self.my_form = FormManager(self.screen, {"username": {"position": (10, 10, 200, 30), "color": Color.WHITE},
                                                 "password": {"position": (10, 70, 200, 30), "color": Color.WHITE}})
        self.trans = Transition(screen=self.screen, resolution=self.resolution)

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
        # pygame.display.flip()
        # Add login panel background
        self.blur = blur_screen(screen=self.screen.copy())



        panel_shape = self.resolution[0] * 0.9, self.resolution[1] * 0.6
        login_panel = morph_image(self.pth_re + "login_box.png", panel_shape)
        register_panel = morph_image(self.pth_re + "register_box.png", panel_shape)
        self.login_panel = add_element(self.blur, login_panel, (
            (self.resolution[0] - panel_shape[0]) / 2, (self.resolution[1] - panel_shape[1]) / 2))
        self.register_panel = add_element(self.blur, register_panel, (
            (self.resolution[0] - panel_shape[0]) / 2, (self.resolution[1] - panel_shape[1]) / 2))
        # self.create_font()  # Create font for text input



        running = True
        # self.trans.descending_circle(pos=(12 * 40 + 20, 12 * 40 + 20), )
        # self.trans.ascending_circle(pos=(12 * 40 + 20, 12 * 40 + 20), )
        pygame.display.flip()
        while running:
            events = pygame.event.get()
            self.my_form.update(events)
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.my_form.focus(pygame.mouse.get_pos())

                if event.type == pygame.QUIT:
                    running = False
                    # pygame.quit()
                    return False  # Fucking transmit signal to another scene here, this is just a prototype
                if event.type == pygame.KEYDOWN:
                    pressed = event.key
                    if self.player.handle_event(pressed):  # Handle interact from player
                        pass
                    if self.player.get_grid_pos() in self.door_pos:
                        self.toggle_panel(event, self.door_pos[self.player.get_grid_pos()])
                        continue
                    self.player.update(
                        self.screenCopy)  # NEED TO OPTIMIZED, https://stackoverflow.com/questions/61399822/how-to-move-character-in-pygame-without-filling-background

    def toggle_panel(self, event, name):
        """
        :param event:
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:
            self.player.deactivate(active=False)

            if name == "Login":
                username, pwd = self.login(event)
            if name == "Exit":
                # Play outro animation here
                pygame.quit()
                exit()
            if name == "Register":
                self.register(event)
                pass

    def login(self, event):
        """
        Login panel
        """

        self.screen.blit(self.login_panel, (0, 0))
        self.my_form.draw()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(self.my_form.get_all_text())
                with open('user_profile.json', 'a+') as file:
                    json.dump(self.my_form.get_all_text(), file)
        pygame.display.update()

        return "username", "password"

    def register(self, event):
        """
        Register panel
        :return: username and password
        """

        self.screen.blit(self.register_panel, (0, 0))
        self.my_form.draw()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print(self.my_form.get_all_text())
                with open('user_profile.json', 'a+') as file:
                    json.dump(self.my_form.get_all_text(), file)
        pygame.display.update()

        pass
