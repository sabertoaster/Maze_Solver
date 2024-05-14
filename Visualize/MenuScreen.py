import pygame
import pygame.locals as pl
from pygame_textinput import TextInputVisualizer, TextInputManager
import numpy as np
import cv2
from Visualize.ImageProcess import blur_screen
from Visualize.ImageProcess import morph_image
from Visualize.ImageProcess import add_element
from Visualize.Transition import Transition
from Visualize.MouseEvents import MouseEvents
from Visualize.HangingSign import HangingSign

from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH, COLORS, SOUNDS

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
            pygame.draw.rect(screen, COLORS['WHITE'], rect, 1)


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
        self.screen = screen
        
        self.sounds_handler = sounds_handler
        
        # Transition effect
        self.transition = Transition(self.screen, RESOLUTION)
        self.sign = HangingSign(SCENE_NAME.upper(), 50)

    def play(self, player):
        """
        Play the scene
        :param player:
        :return:
        """

        # Background and stuff go here
        self.screen.blit(self.frame, (0, 0))
        pygame.display.flip()

        self.sounds_handler.play_bgm(SCENES[SCENE_NAME]['BGM'])


        self.player = player
        self.screenCopy = self.screen.copy()
        self.player.update(self.screenCopy)
        # Add login panel background
        self.blur = blur_screen(screen=self.screen.copy())
        

        self.mouse_handler = MouseEvents(self.screen, self.player, self.frame)
        
        self.chosen_obj = None
        self.chosen_door = None
        self.hovered_obj = None
        
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.transition.transition(pos=(self.player.visual_pos[0] + SCENES[SCENE_NAME]["cell"][0] / 2,
                                self.player.visual_pos[1] + SCENES[SCENE_NAME]["cell"][1] / 2),
                            transition_type='circle_in')
                    return None, None
                
                if self.chosen_door:
                    next_scene, next_grid_pos = self.toggle_panel(self.chosen_door)

                    if next_scene:
                        return next_scene, next_grid_pos
                
                if self.chosen_obj:
                    self.object_handler(self.chosen_obj)
                    self.chosen_obj = None
                    
                mouse_pos = pygame.mouse.get_pos()
                
                self.mouse_handler.set_pos(mouse_pos)

                self.screenCopy, self.hovered_obj = self.mouse_handler.get_hover_frame(self.screenCopy, self.hovered_obj)

                if event.type == pygame.MOUSEBUTTONUP:
                    self.chosen_door, self.chosen_obj = self.mouse_handler.click()
                    events.append(pygame.event.Event(pygame.USEREVENT, {}))
                    continue
                
                if event.type == pygame.KEYDOWN:
                    pressed = event.key
                    player_response = self.player.handle_event(pressed)
                    if player_response == "Move":
                        pass
                    if player_response == "Interact":
                        pass  # Handle Interact Here
                    if player_response == "Door":
                        self.chosen_door = SCENES[SCENE_NAME]['DOORS'][self.player.get_current_door()]
                        

                    self.player.update(self.screenCopy)

    def object_handler(self, object):
        """
        Handle object
        :param object:
        :return:
        """
        if object == 'Music_box':
            self.sounds_handler.switch()

    def toggle_panel(self, name):
        """
        :param name: to know whether if the player step into which door
        :return:
        """
        if name:
            
            self.player.re_init(name=self.player.name, scene=name)
            
            if name == "Login":
                self.transition.transition(pos=(self.player.visual_pos[0] + SCENES[SCENE_NAME]["cell"][0] / 2,
                                                self.player.visual_pos[1] + SCENES[SCENE_NAME]["cell"][1] / 2),
                                           transition_type='circle_in')

                return name, self.player.get_GridMapObject_Player("Login")

            if name == "Leaderboard":
                self.player.update(self.screen)
                
                self.transition.transition(transition_type='zelda_rl', next_scene=name)

                return name, (13, self.player.get_grid_pos()[1])

            if name == "Play":
                self.player.update(self.screen)

                self.transition.transition(transition_type='zelda_lr', next_scene=name)

                return name, (1, self.player.get_grid_pos()[1])
            
        return None, None
