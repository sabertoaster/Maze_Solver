import pygame
import cv2

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH
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
        self.screen = screen    
        self.sounds_handler = sounds_handler

    def play(self, background=None):
        """
        Play the scene
        """
        
        video = cv2.VideoCapture("Resources/animation/win.mp4")
        success, video_image = video.read()
        fps = video.get(cv2.CAP_PROP_FPS)

        clock = pygame.time.Clock()
        pygame.event.clear()
        pygame.key.set_repeat()
        run = success
        first = True
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
                if first:
                    first = False
                    continue
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    run = False
                    break
                
            success, video_image = video.read()
            if success:
                video_image = cv2.resize(video_image, (RESOLUTION[0], RESOLUTION[1]))
                video_surf = pygame.image.frombuffer(
                    video_image.tobytes(), video_image.shape[1::-1], "BGR")
            else:
                run = False
            self.screen.blit(video_surf, ((RESOLUTION[0] - video_surf.get_width()) / 2, (RESOLUTION[1] - video_surf.get_height()) / 2))
            pygame.display.flip()
            
        pygame.key.set_repeat(200, 125)
        
        if background:
            self.screen.blit(background, (0, 0))
    
        return "Menu", SCENES["Menu"]["initial_pos"]
