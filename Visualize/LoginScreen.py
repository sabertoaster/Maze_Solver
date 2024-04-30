import pygame
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
        resolution, cell = res_cel
        self.frame = morph_image(path_resources + FILENAME, resolution)
        self.screen = screen

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """

        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        # drawGrid(screen=self.screen)

        self.panel_fl = True
        self.screenCopy = self.screen.copy()
        self.tempScreen = self.screenCopy.copy()
        self.blur = blur_screen(screen=self.screen)
        player.update(self.screenCopy)
        pygame.display.flip()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    # pygame.quit()
                    return False  # Fucking transmit signal to another scene here, this is just a prototype
                if event.type == pygame.KEYDOWN:
                    pressed = pygame.key.get_pressed()
                    player.handle_event(pressed)
                    if event.key == pygame.K_e and self.panel_fl:
                        self.tempScreen = self.screenCopy.copy()
                        self.screenCopy = self.blur
                        self.toggle_panel("Login")
                        self.panel_fl = not self.panel_fl
                        player.deactivate()
                    elif event.key == pygame.K_e and not self.panel_fl:
                        self.screenCopy = self.tempScreen.copy()
                        self.toggle_panel("Login")
                        self.panel_fl = not self.panel_fl
                        player.deactivate()
                    player.update(self.screenCopy)     # NEED TO OPTIMIZED, https://stackoverflow.com/questions/61399822/how-to-move-character-in-pygame-without-filling-background
            # self.screen.blit(self.frame, (0, 0))
            # pygame.display.flip()
            # for key, val in kwargs:
            #     screen.blit(val, (0, 0))
            #     pygame.display.flip()
            #     self.clock.tick(900)

    def toggle_panel(self, name):
        # self.screen.blit(blur_screen(screen=self.screen), (0, 0))
        # pygame.display.flip()
        return

    def login(self):
        pass

    def register(self):
        pass