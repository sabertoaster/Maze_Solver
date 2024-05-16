import pygame

from CONSTANTS import FONTS, RESOLUTION, COLORS, CREDIT as SECTIONS

#size
SCREEN_WIDTH, SCREEN_HEIGHT = RESOLUTION[0], RESOLUTION[1]
BOX_LENGTH = 1.5
HEADER_FONT_SIZE = SCREEN_HEIGHT // 25
CONTENT_FONT_SIZE = SCREEN_HEIGHT // 35
VERTICAL_SPACING = CONTENT_FONT_SIZE * 2.1
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
        
        #initialize the position of the last text
        
        self.heads = []
        self.bodies = []
        space = 0
        lines = 0
        minus = 0
        self.last_pos = 0
        for head, body in boxes.items():
            if head != "":
                minus = 0
                self.heads.append(Text(head, content_font, (position[0], position[1] + space*VERTICAL_SPACING + lines*CONTENT_FONT_SIZE), CONTENT_HEAD_FONT_COLOR))
            else:
                minus = -CONTENT_FONT_SIZE
            #check if body is an array
            if type(body) == list:
                for content in body:
                    if content != "":
                        self.bodies.append(Text(content, content_font, (position[0], position[1] + minus + space*VERTICAL_SPACING + lines*CONTENT_FONT_SIZE + CONTENT_FONT_SIZE*1.1), CONTENT_FONT_COLOR))
                    lines += 1
            else:
                if body != "":
                    self.bodies.append(Text(body, content_font, (position[0], position[1] + minus + space*VERTICAL_SPACING + lines*CONTENT_FONT_SIZE + CONTENT_FONT_SIZE*1.1), CONTENT_FONT_COLOR))
                lines += 1
            self.last_pos += VERTICAL_SPACING
            space += 1
            
        space -= 1
        self.last_pos = position[1] + space*VERTICAL_SPACING + minus + lines*CONTENT_FONT_SIZE + CONTENT_FONT_SIZE*1.1 - SCREEN_HEIGHT
    
    def get_last_pos(self):
        return self.last_pos
class Section:
    def __init__(self, header_text, content_texts, initial_y):

        self.header = Text(header_text, header_font, (SCREEN_WIDTH // 2, initial_y), HEADER_FONT_COLOR)
        self.contents = Box((SCREEN_WIDTH // 2,  initial_y + VERTICAL_SPACING), content_texts)
        self.next_pos = self.contents.get_last_pos()

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
    
    def get_next_pos(self):
        return self.next_pos

class Credit:
    def __init__(self):
        self.sections = []
        next_pos = 0
        for section_name, content in SECTIONS.items():
            section = Section(section_name, content, SCREEN_HEIGHT + next_pos)
            self.sections.append(section)
            next_pos = section.get_next_pos() + VERTICAL_SPACING
            # if i >= 0:
            #     self.sections.append(Section(section_name, content, space * VERTICAL_SPACING + (lines - 2*box_num)*(CONTENT_FONT_SIZE + CONTENT_FONT_SIZE*1.1) + i*HEADER_FONT_SIZE))
            # else:
            #     self.sections.append(Section(section_name, content, space * VERTICAL_SPACING + (lines - 2*box_num)*(CONTENT_FONT_SIZE + CONTENT_FONT_SIZE*1.1)))
            # print('section space: ', space * VERTICAL_SPACING + (lines - 2*box_num)*(CONTENT_FONT_SIZE + CONTENT_FONT_SIZE*1.1) + i*HEADER_FONT_SIZE)
            # current_box_num = len(content)
            # box_num += current_box_num
            # space += current_box_num*2
            # space += 1
            # for key, value in content.items():
            #     if type(value) == list:
            #         lines += len(value)
            #     elif value != "":
            #         lines += 1
            #     if key != "": 
            #         lines += 1
            # i += 1

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