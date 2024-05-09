import cv2
import numpy
import pygame
from Visualize.ImageProcess import morph_image

class HangingSign:
    def __init__(self, screen, position, text, font_size):
        self.screen = screen
        self.position = position
        self.text = text
        self.font_size = font_size
        self.font = pygame.font.Font('Visualize/Resources/Fonts/PixeloidSans.ttf', font_size)
        self.text_surface = self.font.render(text, True, (0, 0, 0))
        self.sign = morph_image("Visualize/Resources/sign_box.png", (192, 150))

    def change_text(self, text):
        self.text = text
        self.text_surface = self.font.render(text, True, (0, 0, 0))

    def display(self):
        self.screen.blit(self.sign, self.position)
        self.screen.blit(self.text_surface, self.position)

    def display_for_time(self, time):
        pass

