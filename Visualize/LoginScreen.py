import pygame
import pygame.locals as pl
# from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
from Visualize.morph_image import blur_screen
from Visualize.morph_image import morph_image

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
    blockSize = PARAMS["cell"][0]  # Set the size of the grid block
    for x in range(0, PARAMS["resolution"][0], blockSize):
        for y in range(0, PARAMS["resolution"][1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, WHITE, rect, 1)


# [PROTOTYPE]

class LoginScreen:
    def __init__(self, screen, res_cel, path_resources):
        self.resolution, self.cell = res_cel
        self.frame = morph_image(path_resources + FILENAME, self.resolution)
        self.pth_re = path_resources
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
        self.panel_fl = True
        self.screenCopy = self.screen.copy()
        self.tempScreen = self.screenCopy.copy()
        self.blur = blur_screen(screen=self.screen)
        self.player.update(self.screenCopy)
        pygame.display.flip()

        running = True
        while running:
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
                        self.toggle_panel(event, self.door_pos[self.player.get_grid_pos()])
                    self.player.update(
                        self.screenCopy)  # NEED TO OPTIMIZED, https://stackoverflow.com/questions/61399822/how-to-move-character-in-pygame-without-filling-background



            # self.screen.blit(self.frame, (0, 0))
            # pygame.display.flip()
            # for key, val in kwargs:
            #     screen.blit(val, (0, 0))
            #     pygame.display.flip()
            #     self.clock.tick(900)

    def toggle_panel(self, event, name):
        # self.screen.blit(blur_screen(screen=self.screen), (0, 0))
        # pygame.display.flip()
        if name:
            if self.panel_fl:
                self.tempScreen = self.screenCopy.copy()
                self.screenCopy = self.blur
                self.screen = self.screenCopy.copy()
                self.panel_fl = not self.panel_fl
                self.player.deactivate()

                if name == "Login":
                    username, pwd = self.login()
                if name == "Exit":
                    # Play outro animation here
                    pygame.quit()
                    exit()
                if name == "Register":
                    pass

            elif self.panel_fl:
                self.screenCopy = self.tempScreen.copy()
                self.panel_fl = not self.panel_fl
                self.player.deactivate()

    def login(self):
        login_panel = morph_image(self.pth_re + "login_box.png", (self.resolution[1], self.resolution[1]))
        self.screen.blit(login_panel, (0, 0))
        pygame.display.flip()
        self.screenCopy = self.screen.copy()
        return "username", "password"

    def register(self):
        pass
