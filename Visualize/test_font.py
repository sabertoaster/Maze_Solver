# import pygame module # import sys library
import pygame
import sys

# import pygame
#
# pygame.init()
# window = pygame.display.set_mode((500, 300))
# clock = pygame.time.Clock()
# font = pygame.font.SysFont(None, 150)
#
# text_surf = font.render('test', True, (255, 0, 0))
# text_surf.set_alpha(127)
#
# background = pygame.Surface(window.get_size())
# ts, w, h, c1, c2 = 50, *window.get_size(), (128, 128, 128), (64, 64, 64)
# tiles = [((x*ts, y*ts, ts, ts), c1 if (x+y) % 2 == 0 else c2) for x in range((w+ts-1)//ts) for y in range((h+ts-1)//ts)]
# for rect, color in tiles:
#     pygame.draw.rect(background, color, rect)
#
# run = True
# while run:
#     clock.tick(60)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#
#     window.blit(background, (0, 0))
#     window.blit(text_surf, text_surf.get_rect(center = window.get_rect().center))
#     pygame.display.flip()
#
# pygame.quit()
# exit()



# class InputBox:
#     def __init__(self, x, y, w, h, screen, text=''):
#         self.rect = pygame.Rect(x, y, w, h)
#         self.font = pygame.font.Font("Resources/Fonts/arial.ttf", h - 5)
#         self.color = (255, 255, 255, 1)
#         self.txt_surface = self.font.render(text, True, self.color)
#         self.txt_surface.set_alpha(127)
#         pygame.draw.rect(screen, self.color, self.rect)
#         self.text = text
#         self.active = False
#         self.screen = screen
#
#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             # If the user clicked on the input_box rect.
#             if self.rect.collidepoint(event.pos):
#                 # Toggle the active variable.
#                 self.active = not self.active
#             else:
#                 self.active = False
#             # Change the current color of the input box.
#             self.color = (255, 255, 255) if self.active else (0, 0, 0)
#
#         if event.type == pygame.KEYDOWN:
#             if self.active:
#                 if event.key == pygame.K_BACKSPACE:
#                     self.text = self.text[:-1]
#                     self.txt_surface = self.font.render(self.text, True, self.color)
#                 else:
#                     if event.key == pygame.K_RETURN:
#                         print(self.text)
#                         self.text = ''
#                     elif event.key == pygame.K_BACKSPACE:
#                         self.text = self.text[:-1]
#                     else:
#                         self.text += event.unicode
#                 # Re-render the text.
#                 self.txt_surface = self.font.render(self.text, True, self.color)
#                 self.update()
#
#     def update(self):
#         # Resize the box if the text is too long.
#         self.draw()
#         width = min(250, max(200, self.txt_surface.get_width() + 10))
#         self.rect.w = width
#         print(self.rect.w)
#         self.draw()
#
#     def draw(self):
#         # Black background
#         black_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, self.rect.w + self.txt_surface.get_width(), self.rect.h + 15)
#         pygame.draw.rect(self.screen, (0, 0, 0, 0), black_rect)
#         # Blit the text.
#         self.screen.blit(self.txt_surface, (self.rect.x, self.rect.y))
#         # Blit the rect.
#         pygame.draw.rect(self.screen, self.color, self.rect, 1)
#         pygame.display.flip()
#
# # initializing pygame
# pygame.init()
# clock = pygame.time.Clock()
#
# background = pygame.rect.Rect(0, 0, 500, 500)
#
# display_screen = pygame.display.set_mode((500, 500))
# pygame.draw.rect(display_screen, (255, 255, 255), background)
#
# input_1 = InputBox(100, 100, 200, 32, screen=display_screen)
# input_2 = InputBox(100, 200, 200, 32, screen=display_screen)
#
#
# # add font style and size
# base_font = pygame.font.Font("Resources/Fonts/arial.ttf", 40)
# # set left, top, width, height in
# # Pygame.Rect()
# # color_passive = pygame.Color("gray15")
# # color_active = pygame.Color("lightskyblue")
#
# # input_rect = pygame.Rect(100, 100, 140, 32)
# # color = color_passive
# # active = False
# #
# # input_rect_2 = pygame.Rect(200, 200, 140, 32)
# # color_2 = color_passive
# # active_2 = False
#
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#         input_1.handle_event(event)
#         input_2.handle_event(event)
#     input_1.draw()
#     input_2.draw()
#         # # when mouse collides with the rectangle
#         # # make active as true
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         #     if input_rect.collidepoint(event.pos):
#         #         active = not active
#         #     if input_rect_2.collidepoint(event.pos):
#         #         active_2 = not active_2
#         #
#         # # if the key is physically pressed down
#         # if event.type == pygame.KEYDOWN:
#         #     if event.key == pygame.K_BACKSPACE:
#         #
#         #         # stores text except last letter
#         #         user_text = user_text[0:-1]
#         #     else:
#         #         user_text += event.unicode
#     clock.tick(60)

import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
pygame.init()

# No arguments needed to get start
textinput = TextInputVisualizer()

# But more customization possible: Pass your own font object
font = pygame.font.Font("Resources/Fonts/PixeloidSans.ttf", 55)
# Create own manager with custom input validator
manager = TextInputManager(validator=lambda input: len(input) <= 10)
# Pass these to constructor
textinput_custom = TextInputVisualizer(manager=manager, font_object=font)
# Customize much more
textinput_custom.cursor_width = 4
textinput_custom.cursor_blink_interval = 400  # blinking interval in ms
textinput_custom.antialias = False
textinput_custom.font_color = (0, 85, 170)

screen = pygame.display.set_mode((1000, 200))
clock = pygame.time.Clock()

# Pygame now allows natively to enable key repeat:
pygame.key.set_repeat(200, 25)

while True:
    screen.fill((225, 225, 225))

    events = pygame.event.get()

    # Feed it with events every frame
    textinput.update(events)
    textinput_custom.update(events)

    # Get its surface to blit onto the screen
    # screen.blit(textinput.surface, (10, 10))
    screen.blit(textinput_custom.surface, (10, 50))

    # Modify attributes on the fly - the surface is only rerendered when .surface is accessed & if values changed
    # textinput_custom.font_color = [(c + 10) % 255 for c in textinput_custom.font_color]

    # Check if user is exiting or pressed return
    for event in events:
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            print(f"User pressed enter! Input so far: {textinput_custom.value}")

    pygame.display.update()
    clock.tick(30)
