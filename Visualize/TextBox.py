import pygame
from pygame_textinput import TextInputManager, TextInputVisualizer
from typing import Dict

from CONSTANTS import FONTS, COLORS as Color

class TextBox:
    def __init__(self, screen, position, font_color, manager, text='', focusable=True, background=None):
        (x, y, width, height) = position
        self.screen = screen
        self.height = height
        self.x = x
        self.y = y

        self.width = width
        self.height = height
        self.bg_color = background  # Background color here
        # self.rect = pygame.Rect(x, y, width, height)
        self.active = False
        self.focusable = focusable
        font = pygame.font.Font(FONTS['default'], height - 5)
        self.text_input = TextInputVisualizer(manager=manager, font_object=font, cursor_blink_interval=400,
                                              font_color=font_color)
        self.text_input._require_rerender()
        # Customize much more
        self.text_input.value = text
        self.text_input.cursor_width = 5
        # self.text_input.cursor_color = font_color
        self.text_input.antialias = True

    def get_position(self):
        return self.x, self.y, self.width, self.height

    def set_position(self, position):
        self.x = position[0]
        self.y = position[1]

    def set_size(self, size):
        self.width = size[1]
        self.height = size[0]

    def set_text(self, text):
        self.text_input.value = text

    def get_current_text(self):
        return self.text_input.value

    def get_length(self):
        font = pygame.font.Font(FONTS['default'], self.height - 5)
        text_surface = font.render(self.text_input.value, True, Color.BLACK.value)
        return text_surface.get_width()

    def draw(self, background=False):
        self.text_input._rerender()
        if background:
            width = self.get_length()
            box = pygame.Surface((width, self.height * 1.2), pygame.SRCALPHA)
            box.fill((0, 0, 0, 128))
            self.screen.blit(box, (self.x, self.y))
        self.screen.blit(self.text_input.surface, (self.x, self.y))
        
    def get_text(self):
        return self.text_input.value
    
    def set_color(self, color):
        self.text_input.font_color = color

    def draw_on_minimap(self, screen, background=False):
        self.text_input._rerender()
        if background:
            width = self.get_length()
            box = pygame.Surface((width, self.height * 1.2), pygame.SRCALPHA)
            box.fill((0, 0, 0, 128))
            screen.blit(box, (self.x, self.y))
        screen.blit(self.text_input.surface, (self.x, self.y))


class FormManager:
    """
    This is a class to represent Form Manager Instance
    """

    def __init__(self, screen, list_of_textbox: [str, {"position": (int, int, int, int), "color": Color,
                                                       "maximum_length": int, "focusable": bool,
                                                       "init_text": str}]):
        """
        Initialize Form Manager Instance
        :param screen: pygame.Surface
        :param list_of_textbox: Dict[str, {"position": (int, int, int, int), "color": Color, "maximum_length": int, "controllable": bool,
              "init_text": str}]
        "focusable": có thể focus
        "init_text": giá trị ban đầu của textbox
        """
        self.text_boxes = dict.fromkeys(list_of_textbox.keys())
        for key, value in list_of_textbox.items():
            self.text_boxes[key] = {
                "box": TextBox(screen=screen, position=value["position"], font_color=value["color"],
                               manager=TextInputManager(validator=lambda input_s: len(input_s) <= value["maximum_length"]),
                               text=value["init_text"], focusable=value["focusable"])}

    def focus(self, position: object) -> None:
        """
        Handle focus event
        """
        for key, value in self.text_boxes.items():
            if not value["box"].focusable:
                continue
            (x, y, width, height) = value["box"].get_position()
            if x <= position[0] <= x + width and y <= position[1] <= y + height:
                value["box"].active = True
                value["box"].text_input.cursor_visible = True
            else:
                value["box"].active = False
                value["box"].text_input.cursor_visible = False

    def update(self, events):
        """
        Update text input
        """
        for key, value in self.text_boxes.items():
            if value["box"].active:
                value["box"].text_input.update(events)

    def draw(self):
        """
        Draw text input
        """
        for key, value in self.text_boxes.items():
            if key == "password":
                tmp = value["box"].get_text()
                value["box"].set_text("*" * len(value["box"].get_current_text()))
                value["box"].draw()
                value["box"].set_text(tmp)
                continue
            value["box"].draw()

    def set_text(self, key, text) -> None:
        """
        Set text for text input
        key: str -> name of text box
        """
        self.text_boxes[key]["box"].set_text(text)
        
    def set_color(self, key, color):
        self.text_boxes[key]["box"].set_color(color)

    def get_current_text(self) -> Dict[str, str]:
        """
        Get current text from text input
        """
        return {key: value["box"].get_current_text() for key, value in self.text_boxes.items() if
                value["box"].active}

    def get_all_text(self) -> Dict[str, str]:
        """
        Get all text from text input
        """
        return {key: value["box"].get_current_text() for key, value in self.text_boxes.items()}

    def get_textbox(self, key):
        return self.text_boxes[key]["box"]
    

