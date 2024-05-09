import cv2
import numpy
import pygame

class HangingSign:
    def __init__(self, text, font_size):

        self.text_font = pygame.font.Font('Visualize/Resources/Fonts/PixeloidSansBold.ttf', font_size)
        # self.border_font = pygame.font.Font('Visualize/Resources/Fonts/PixeloidSansBold.ttf', font_size + 5)

        self.text_surface = self.text_font.render(text, True, (0, 0, 0))
        # self.border_surface = self.border_font.render(text, True, (0, 0, 0))

        self.sign = pygame.image.load("Visualize/Resources/" + "sign_box.png").convert_alpha()

        # self.sign.blit(self.border_surface,
        #                (self.sign.get_width() // 2 - self.border_surface.get_width() // 2,
        #                 (60 + 186 - self.border_surface.get_height()) / 2))
        self.sign.blit(self.text_surface,
                       (self.sign.get_width() // 2 - self.text_surface.get_width() // 2,
                        (60 + 186 - self.text_surface.get_height()) / 2))



    def to_surface(self):
        return self.sign

    def display_for_time(self, time):
        pass

