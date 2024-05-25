import pygame

from CONSTANTS import RESOURCE_PATH, FONTS

RESOURCE_PATH += 'img/'

class HangingSign:
    def __init__(self, text, font_size):
        
        self.text_font = pygame.font.Font(FONTS['default_bold'], font_size)
        self.text = self.text_font.render(text, True, (0, 0, 0))

        self.sign = pygame.image.load(RESOURCE_PATH + "sign_box.png").convert_alpha()

        self.sign.blit(self.text,
                       (self.sign.get_width() // 2 - self.text.get_width() // 2,
                        (60 + 186 - self.text.get_height()) / 2))

    def to_surface(self):
        return self.sign
