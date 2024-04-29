import pygame
import cv2
from Visualize.morph_image import morph_image

FILENAME = "login_prototype.jpg"


class LoginScreen:
    def __init__(self, screen, resolution, path_resources):
        self.frame = morph_image(path_resources + FILENAME, resolution)
        self.screen = screen

    def play(self, **kwargs):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            # self.screen.blit(self.frame, (0, 0))
            # pygame.display.flip()
            # for key, val in kwargs:
            #     screen.blit(val, (0, 0))
            #     pygame.display.flip()
            #     self.clock.tick(900)