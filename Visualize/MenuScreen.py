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


SCENE_NAME = "Menu"

def drawGrid(screen):
    """
    FOR FUCKING DEBUG THE GRID MAP
    :param screen:
    :return:
    """
    blockSize = SCENES[SCENE_NAME]["cell"][0]  # Set the size of the grid block
    for x in range(0, RESOLUTION[0], blockSize):
        for y in range(0, RESOLUTION[1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, COLORS.WHITE.value, rect, 1)


# [PROTOTYPE]

class MenuScreen:
    """
    This is a class to manage Login Screen Instance, (Pokémon theme)
    """
    def __init__(self, screen, sounds_handler):
        """
        :param screen:
        :param res_cel:
        :param path_resources:
        """

        self.frame = morph_image(RESOURCE_PATH + SCENES[SCENE_NAME]["BG"], RESOLUTION)
        self.instructions_frame = morph_image(RESOURCE_PATH + SCENES[SCENE_NAME]['BG_instructions'], RESOLUTION)
        self.screen = screen
        
        self.sounds_handler = sounds_handler
        
        # Transition effect
        self.transition = Transition(self.screen, RESOLUTION, sounds_handler=self.sounds_handler)
        
        self.sign = HangingSign(SCENE_NAME.upper(), 50)
        self.screenBlur = blur_screen(self.screen)
        
        self.credit = Credit(sounds_handler=self.sounds_handler)

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """

        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        pygame.display.flip()
        # drawGrid(self.screen)

        self.player = player
        self.player.re_init(name=self.player.name, scene=SCENE_NAME)
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background
        self.blur = blur_screen(screen=self.screen.copy())
        print('Previous scene:', self.player.previous_scene)
        if self.player.previous_scene == "Login":
            self.transition.transition(transition_type='sign_pop', box=self.sign)
        
        # Play BGM
        self.sounds_handler.play_bgm(SCENE_NAME)

        self.show_instructions = [False]

        self.mouse_handler = MouseEvents(self.screen, self.player, self.frame, self.show_instructions)
        
        self.chosen_obj = None
        self.chosen_door = None
        self.hovered_obj = None


        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                                
                mouse_pos = pygame.mouse.get_pos()
                
                if event.type == pygame.QUIT:
                    return None, None
                
                if self.chosen_door:
                    next_scene, next_grid_pos = self.toggle_panel(self.chosen_door)
                    if next_scene:
                        return next_scene, next_grid_pos
                
                if self.chosen_obj:
                    self.handle_object(self.chosen_obj)
                    self.chosen_obj = None
                    continue
                                    
                self.mouse_handler.set_pos(mouse_pos)

                self.screenCopy, self.hovered_obj = self.mouse_handler.get_hover_frame(self.screenCopy, self.hovered_obj)
                
                if event.type == pygame.MOUSEBUTTONUP:
                    self.chosen_door, self.chosen_obj = self.mouse_handler.click()
                    events.append(pygame.event.Event(pygame.USEREVENT, {}))
                    continue
                
                if event.type == pygame.KEYDOWN:
                
                    pressed = event.key
                    
                    if pressed == pygame.K_m:
                        self.sounds_handler.switch()
                        continue
                    
                    if pressed == pl.K_SPACE:
                        if not self.show_instructions[0]:
                            self.screen.blit(self.instructions_frame, (0, 0))
                            self.screenCopy = self.screen.copy()
                            self.player.update(self.screen.copy())
                            pygame.display.flip()
                            
                            self.show_instructions[0] = True
                            
                            continue
                        else:
                            self.screen.blit(self.frame, (0, 0))
                            self.screenCopy = self.screen.copy()
                            self.player.update(self.screen.copy())
                            pygame.display.flip()
                            
                            self.show_instructions[0] = False
                            
                            continue
                    
                    player_response = self.player.handle_event(pressed)
                    if player_response == "Move":
                        pass
                    if player_response == "Interact":
                        self.chosen_obj = self.player.interacted_obj
                        if self.chosen_obj:
                            events.append(pygame.event.Event(pygame.USEREVENT, {}))
                            continue
                    if player_response == "Door":
                        self.chosen_door = SCENES[SCENE_NAME]['DOORS'][self.player.get_current_door()]

                    self.player.update(self.screenCopy)

    def handle_object(self, object):
        """
        Handle object
        :param object:
        :return:
        """
        if object == 'Music_box':
            self.sounds_handler.switch()
        if object == "Skin":
            self.player.switch_skin(self.player.skin)
            self.screen.blit(self.frame, (0, 0))
            self.player.update(self.screenCopy)
        if object == "Credit":
            self.player.update(self.screenCopy)
            self.credit.play_credit_sence(screen=self.screen, blur=blur_screen(self.screen))
            self.player.update(self.screenCopy)


    def toggle_panel(self, name):
        """
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:
                        
            if name == "Login":
                self.transition.transition(pos=(self.player.visual_pos[0] + SCENES[SCENE_NAME]["cell"][0] / 2,
                                                self.player.visual_pos[1] + SCENES[SCENE_NAME]["cell"][1] / 2),
                                           transition_type='circle_in')

                # Player re-init
                self.player.deactivate(active=True)
                self.player.re_init(name="Guest", scene=name, dir='down')
                    
                return name, self.player.get_GridMapObject_Player("Login")

            if name == "Leaderboard":
                self.player.update(self.screen)
                self.transition.transition(transition_type='zelda_rl', next_scene=name)
                
                if self.player.get_grid_pos()[1] == 2:
                    return name, (13, self.player.get_grid_pos()[1] + 1)
                
                # Player re-init
                self.player.deactivate(active=True)
                self.player.re_init(name=self.player.name, scene=name, dir='left')
                    
                return name, (13, self.player.get_grid_pos()[1])

            if name == "Play":
                self.player.update(self.screen)

                self.transition.transition(transition_type='zelda_lr', next_scene=name)

                # Player re-init
                self.player.deactivate(active=True)
                self.player.re_init(name=self.player.name, scene=name, dir='right')

                return name, (1, self.player.get_grid_pos()[1])
            
        return None, None


        
        


