import pygame
from pygame_textinput import TextInputManager, TextInputVisualizer
from typing import Dict
from enum import Enum
import numpy
import cv2

DEFAULT_FONT_PATH = 'Visualize/Resources/Fonts/PixeloidSans.ttf'


class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)


class TextBox:
    def __init__(self, screen, position, font_color, manager, text=''):
        (x, y, width, height) = position
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = (255, 255, 255)  # Background color here
        self.rect = pygame.Rect(x, y, width, height)
        self.active = False

        font = pygame.font.Font(DEFAULT_FONT_PATH, height - 5)
        self.text_input = TextInputVisualizer(manager=manager, font_object=font, cursor_blink_interval=400)
        # Customize much more
        self.text_input.value = text
        self.text_input.cursor_width = 2
        # self.text_input.cursor_color = font_color
        self.text_input.antialias = True

    def get_position(self):
        return self.x, self.y, self.width, self.height

    def get_current_text(self):
        return self.text_input.value

    def draw(self):
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        self.screen.blit(self.text_input.surface, (self.x, self.y))


class FormManager:
    """
    This is a class to represent Form Manager Instance
    """
    def __init__(self, screen, list_of_textbox: Dict[str, {"position": (int, int, int, int), "color": Color}]):
        """
        Initialize Form Manager Instance
        :param screen: pygame.Surface
        :param list_of_textbox: Dict[str, {"position": (int, int, int, int), "color": Color}]
        """
        self.text_boxes = dict.fromkeys(list_of_textbox.keys())
        for key, value in list_of_textbox.items():
            self.text_boxes[key] = {
                "box": TextBox(screen=screen, position=value["position"], font_color=value["color"],
                               manager=TextInputManager(validator=lambda input_s: len(input_s) <= 14))
            }

    def focus(self, position) -> None:
        for key, value in self.text_boxes.items():
            (x, y, width, height) = value["box"].get_position()
            if x <= position[0] <= x + width and y <= position[1] <= y + height:
                value["box"].active = True
                value["box"].text_input.cursor_visible = True
            else:
                value["box"].active = False
                value["box"].text_input.cursor_visible = False

    def update(self, events):
        for key, value in self.text_boxes.items():
            if value["box"].active:
                value["box"].text_input.update(events)

    def draw(self):
        for key, value in self.text_boxes.items():
            value["box"].draw()

    def get_current_text(self) -> Dict[str, str]:
        return {key: value["box"].get_current_text() for key, value in self.text_boxes.items() if value["box"].active}

    def get_all_text(self) -> Dict[str, str]:
        return {key: value["box"].get_current_text() for key, value in self.text_boxes.items()}