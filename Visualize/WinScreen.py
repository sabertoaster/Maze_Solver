import pygame
import cv2
import numpy as np

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, FONTS, COLORS

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

    def play(self, background=None, mode="Manual", time=0, steps=0, win=False):
        """
        Play the scene
        """
        bold_text_font = pygame.font.Font(FONTS["default_bold"], 100)
        normal_text_font = pygame.font.Font(FONTS["default"], 45)
        video = cv2.VideoCapture("Resources/animation/win.mp4")
        success, video_image = video.read()
        fps = video.get(cv2.CAP_PROP_FPS)

        clock = pygame.time.Clock()
        pygame.event.clear()
        pygame.key.set_repeat()
        
        self.sounds_handler.play_bgm(SCENE_NAME)
        
        run = success
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    break
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
                break
                
            self.screen.blit(video_surf, ((RESOLUTION[0] - video_surf.get_width()) / 2, (RESOLUTION[1] - video_surf.get_height()) / 2))
            text = bold_text_font.render("YOU WIN",
                                   True,
                                   (np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 255)))
            self.screen.blit(text, ((RESOLUTION[0] - text.get_width()) / 2, (RESOLUTION[1] - text.get_height()) / 2))
            pygame.display.flip()

        if background:
            self.screen.blit(background, (0, 0))

        pygame.event.clear()
        
        
        steps_text = normal_text_font.render(f"Steps: {steps}",
                                            True,
                                            COLORS.LIGHT_BLUE.value)
        time_text = normal_text_font.render(f"Time: {time:.2f}s",
                                            True,
                                            COLORS.RED.value)      
        continue_panel = pygame.image.load(RESOURCE_PATH + "continue.png")
        hovered_yes_continue_panel = pygame.image.load(RESOURCE_PATH + SCENES[SCENE_NAME]['HOVER_FRAME']['yes'])
        hovered_no_continue_panel = pygame.image.load(RESOURCE_PATH + SCENES[SCENE_NAME]['HOVER_FRAME']['no'])
        hovered_yes_continue_panel.blit(steps_text, ((RESOLUTION[0] - steps_text.get_width()) / 2 + 150 , (RESOLUTION[1] - steps_text.get_height()) / 2 - 25))
        hovered_yes_continue_panel.blit(time_text, ((RESOLUTION[0] - time_text.get_width()) / 2 - 150, (RESOLUTION[1] - time_text.get_height()) / 2 - 25))
        hovered_no_continue_panel.blit(steps_text, ((RESOLUTION[0] - steps_text.get_width()) / 2 + 150 , (RESOLUTION[1] - steps_text.get_height()) / 2 - 25))
        hovered_no_continue_panel.blit(time_text, ((RESOLUTION[0] - time_text.get_width()) / 2 - 150, (RESOLUTION[1] - time_text.get_height()) / 2 - 25))
        continue_panel.blit(steps_text, ((RESOLUTION[0] - steps_text.get_width()) / 2 + 150 , (RESOLUTION[1] - steps_text.get_height()) / 2 - 25))
        continue_panel.blit(time_text, ((RESOLUTION[0] - time_text.get_width()) / 2 - 150, (RESOLUTION[1] - time_text.get_height()) / 2 - 25))
        self.screen.blit(continue_panel, (
            (RESOLUTION[0] - continue_panel.get_width()) / 2, (RESOLUTION[1] - continue_panel.get_height()) / 2))
        pygame.display.flip()


        idling = True
        mouse_grid_pos = None
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                                    
                mouse_pos = pygame.mouse.get_pos()
                tmp_grid_pos = (mouse_pos[1] // SCENES[SCENE_NAME]['cell'][0], mouse_pos[0] // SCENES[SCENE_NAME]['cell'][1])  
                if tmp_grid_pos != mouse_grid_pos:
                    idling = False
                    mouse_grid_pos = tmp_grid_pos
                else:
                    idling = True
                                  
                key = None
                for i, button in SCENES[SCENE_NAME]['OBJECTS_POS'].items():
                    if mouse_grid_pos in button:
                        key = i
                        break
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if key is not None:
                        pygame.key.set_repeat(200, 125)
                        if key == 'no':
                            self.sounds_handler.play_sfx('interact2')
                            return "Menu", SCENES["Menu"]["initial_pos"]
                        elif key == 'yes':
                            self.sounds_handler.play_sfx('interact2')
                            return "Gameplay", SCENES["Gameplay"]["initial_pos"]
                        
                if key and not idling:
                    hovered = None
                    if key == 'yes':
                        hovered = hovered_yes_continue_panel
                    elif key == 'no':
                        hovered = hovered_no_continue_panel
                        
                    self.screen.blit(hovered, ((RESOLUTION[0] - continue_panel.get_width()) / 2, (RESOLUTION[1] - continue_panel.get_height()) / 2))
                
                elif not idling and not key:
                    self.screen.blit(continue_panel, (
                        (RESOLUTION[0] - continue_panel.get_width()) / 2, (RESOLUTION[1] - continue_panel.get_height()) / 2))
                pygame.display.flip()

        
