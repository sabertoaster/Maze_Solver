import pygame
import cv2

from Visualize.Credit import Credit

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS, FONTS
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

        win_font = pygame.font.Font(FONTS["default_bold"], 100)
        for _ in range(20):
            text = win_font.render("YOU WIN",
                                   True,
                                   (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)))
            window.blit(text, ((RESOLUTION[0] - text.get_width()) / 2, (RESOLUTION[1] - text.get_height()) / 2))
            pygame.display.flip()
            pygame.time.delay(100)
            window.fill((0,0,0))
            pygame.display.flip()
            pygame.time.delay(100)

        pygame.event.clear()
        if_continue = pygame.image.load(RESOURCE_PATH + "continue.png")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    pygame.key.set_repeat(200, 125)
                    return "Menu", SCENES["Menu"]["initial_pos"]
                window.blit(if_continue, (
                (RESOLUTION[0] - if_continue.get_width()) / 2, (RESOLUTION[1] - if_continue.get_height()) / 2))
                pygame.display.flip()

        pygame.key.set_repeat(200, 125)
        
        if background:
            self.screen.blit(background, (0, 0))
    
        return "Menu", SCENES["Menu"]["initial_pos"]
