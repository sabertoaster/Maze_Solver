import pygame

from CONSTANTS import FONTS, RESOLUTION, COLORS, CREDIT as SECTIONS

#size
SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTION[0], RESOLUTION[1]
VERTICAL_SPACING = SCREEN_HEIGHT // 10
BOX_LENGTH = 1.5
HEADER_FONT_SIZE = SCREEN_HEIGHT // 25
CONTENT_FONT_SIZE = SCREEN_HEIGHT // 35
NORMAL_SPEED = 1
FAST_SPEED = 5
FPS = 60

#color 
HEADER_FONT_COLOR = COLORS.CYAN.value
CONTENT_HEAD_FONT_COLOR = COLORS.YELLOW.value
CONTENT_FONT_COLOR = COLORS.WHITE.value

#font
header_font = pygame.font.Font(FONTS["default_bold"], HEADER_FONT_SIZE)
content_font = pygame.font.Font(FONTS["default"], CONTENT_FONT_SIZE)

class Text:
    def __init__(self, text, font, position, color=COLORS.YELLOW.value):
        self.text = text
        self.font = font
        self.position = position
        self.surface = self.font.render(self.text, True, color)
        self.rect = self.surface.get_rect(center=self.position)

    def update(self, speed):
        self.position = (self.position[0], self.position[1] - speed)
        self.rect = self.surface.get_rect(center=self.position)

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        
class Box:
    def __init__(self, position, boxes):
        self.heads = []
        self.bodies = []
        i = 0
        step = 0
        for head, body in boxes.items():
            if head != "":
                self.heads.append(Text(head, content_font, (position[0], position[1] + i*VERTICAL_SPACING*BOX_LENGTH), CONTENT_HEAD_FONT_COLOR))
            if body != "":
                self.bodies.append(Text(body, content_font, (position[0], position[1] + VERTICAL_SPACING//3 + i*VERTICAL_SPACING*BOX_LENGTH), CONTENT_FONT_COLOR))
            i += 1

class Section:
    def __init__(self, header_text, content_texts, initial_y):

        self.header = Text(header_text, header_font, (SCREEN_WIDTH // 2, SCREEN_HEIGHT + initial_y), HEADER_FONT_COLOR)
        self.contents = Box((SCREEN_WIDTH // 2, SCREEN_HEIGHT + initial_y + VERTICAL_SPACING), content_texts)

    def update(self, speed):
        self.header.update(speed)
        for head in self.contents.heads:
            head.update(speed)
        for body in self.contents.bodies:
            body.update(speed)

    def draw(self, screen):
        self.header.draw(screen)
        for head in self.contents.heads:
            head.draw(screen)
        for body in self.contents.bodies:
            body.draw(screen)

class Credit:
    def __init__(self):
        self.sections = []
        i = 0
        for section_name, content in SECTIONS.items():
            self.sections.append(Section(section_name, content, i * VERTICAL_SPACING))
            i += (len(content) + 1)*BOX_LENGTH
    def update(self, speed):
        for section in self.sections:
            section.update(speed)

    def draw(self, screen):
        for section in self.sections:
            section.draw(screen)

def play_credit_sence(credit, screen, blur):
        clock = pygame.time.Clock()

        running = True
        while running:
            speed = NORMAL_SPEED

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                speed = FAST_SPEED
            if keys[pygame.K_ESCAPE]:
                running = False

            screen.blit(blur, (0, 0))

            credit.update(speed)
            credit.draw(screen)

            try:
                if credit.sections[-1].contents.bodies[-1].position[1] < -CONTENT_FONT_SIZE:
                    running = False
            except IndexError:
                try:
                    if credit.sections[-1].contents.heads[-1].position[1] < -CONTENT_FONT_SIZE:
                        running = False
                except IndexError:
                    try:
                        if credit.sections[-1].header.position[1] < -CONTENT_FONT_SIZE:
                            running = False
                    except IndexError:
                        pass
            pygame.display.flip()

            clock.tick(FPS)

# 