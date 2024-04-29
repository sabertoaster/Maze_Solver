# import pygame module # import sys library
import pygame
import sys


class InputBox:
    def __init__(self, x, y, w, h, screen, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.font = pygame.font.Font("Resources/Fonts/arial.ttf", h - 5)
        self.color = pygame.Color("gray15")
        self.txt_surface = self.font.render(text, True, self.color)
        self.text = text
        self.active = False
        self.screen = screen

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pygame.Color("lightskyblue") if self.active else pygame.Color("gray15")

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    self.txt_surface = self.font.render(self.text, True, self.color)
                else:
                    if event.key == pygame.K_RETURN:
                        print(self.text)
                        self.text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)
                self.update()

    def update(self):
        # Resize the box if the text is too long.
        self.draw()
        width = min(250, max(200, self.txt_surface.get_width() + 10))
        self.rect.w = width
        print(self.rect.w)
        self.draw()

    def draw(self):
        # Black background
        black_rect = pygame.Rect(self.rect.x - 1, self.rect.y - 1, self.rect.w + self.txt_surface.get_width(), self.rect.h + 15)
        pygame.draw.rect(self.screen, (0, 0, 0), black_rect)
        # Blit the text.
        self.screen.blit(self.txt_surface, (self.rect.x, self.rect.y))
        # Blit the rect.
        pygame.draw.rect(self.screen, self.color, self.rect, 1)
        pygame.display.flip()

# initializing pygame
pygame.init()
clock = pygame.time.Clock()
display_screen = pygame.display.set_mode((500, 500))


input_1 = InputBox(100, 100, 200, 32, screen=display_screen)
input_2 = InputBox(100, 200, 200, 32, screen=display_screen)


# add font style and size
base_font = pygame.font.Font("Resources/Fonts/arial.ttf", 40)

# stores text taken by keyboard
user_text = ''

# set left, top, width, height in
# Pygame.Rect()
# color_passive = pygame.Color("gray15")
# color_active = pygame.Color("lightskyblue")

# input_rect = pygame.Rect(100, 100, 140, 32)
# color = color_passive
# active = False
#
# input_rect_2 = pygame.Rect(200, 200, 140, 32)
# color_2 = color_passive
# active_2 = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        input_1.handle_event(event)
        input_2.handle_event(event)
    input_1.draw()
    input_2.draw()
        # # when mouse collides with the rectangle
        # # make active as true
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if input_rect.collidepoint(event.pos):
        #         active = not active
        #     if input_rect_2.collidepoint(event.pos):
        #         active_2 = not active_2
        #
        # # if the key is physically pressed down
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_BACKSPACE:
        #
        #         # stores text except last letter
        #         user_text = user_text[0:-1]
        #     else:
        #         user_text += event.unicode
    clock.tick(60)
