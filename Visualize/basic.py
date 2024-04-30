# THIS IS A PROTOTYPE FOR VISUALIZING, PLEASE DO NOT USE THIS FILE IN MAIN SOURCE CODE
# YOU CAN USE THIS FILE STRUCTURE TO BUILD A NEW VISUALIZATION CLASS

import pygame
import cv2

SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 900

class Visualizer():
    def __init__(self, path_resources):
        self.path_resources = path_resources
        self.logo = pygame.image.load(path_resources + "logo.png")

        # create a surface on screen that has the size of 240 x 180
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,  SCREEN_HEIGHT))

        # define a variable to control the main loop
        running = True
        self.clock = pygame.time.Clock()

    def loading(self):
        pygame.init()
        pygame.display.set_icon(self.logo)
        pygame.display.set_caption("Loading")

        img = cv2.imread(self.path_resources + "intro_1.png")
        img = cv2.resize(img, (SCREEN_WIDTH,  SCREEN_HEIGHT))
        img_2 = cv2.imread(self.path_resources + "intro_2.png")
        img_2 = cv2.resize(img_2, (SCREEN_WIDTH,  SCREEN_HEIGHT))
        # loading_1 = pygame.image.load(self.path_resources + "intro_1_scaled_7x_pngcrushed.png").convert()
        # loading_2 = pygame.image.load(self.path_resources + "intro_2_scaled_7x_pngcrushed.png").convert()
        loading_1 = pygame.image.frombuffer(img.tobytes(), img.shape[1::-1], "BGR")
        loading_2 = pygame.image.frombuffer(img_2.tobytes(), img_2.shape[1::-1], "BGR")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
            self.screen.blit(loading_1, (0, 0))
            pygame.display.flip()
            self.clock.tick(900)
            self.screen.blit(loading_2, (0, 0))
            pygame.display.flip()
            self.clock.tick(900)


if __name__=="__main__":
    # call the main function
    ###
    visualizer = Visualizer("Resources/")
    visualizer.loading()
    ###