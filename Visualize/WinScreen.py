import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image, add_element
from Visualize.Transition import Transition
from Visualize.MouseEvents import MouseEvents
from Visualize.HangingSign import HangingSign

from Visualize.Credit import Credit

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS
RESOURCE_PATH += 'img/'

SCENE_NAME = "Win"

class WinScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """
    def __init__(self, screen, sounds_handler):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """



    def play(self, player):
        """
        Play the scene
        """
        video = cv2.VideoCapture("Resources/animation/win.mp4")
        success, video_image = video.read()
        fps = video.get(cv2.CAP_PROP_FPS)

        window = pygame.display.set_mode(RESOLUTION)
        clock = pygame.time.Clock()
        pygame.event.clear()
        pygame.key.set_repeat()
        run = success
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pl.K_ESCAPE:
                        run = False
                        break
                elif event.type == pygame.MOUSEBUTTONUP:
                    run = False
                    break

            success, video_image = video.read()
            if success:
                video_image = cv2.resize(video_image, (RESOLUTION[0], RESOLUTION[1]))
                video_surf = pygame.image.frombuffer(
                    video_image.tobytes(), video_image.shape[1::-1], "BGR")
            else:
                run = False
            window.blit(video_surf, ((RESOLUTION[0] - video_surf.get_width()) / 2, (RESOLUTION[1] - video_surf.get_height()) / 2))
            pygame.display.flip()
            
        pygame.key.set_repeat(200, 125)
        return "Menu", SCENES["Menu"]["initial_pos"]
