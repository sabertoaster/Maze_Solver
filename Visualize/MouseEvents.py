import pygame
from Visualize.ImageProcess import morph_image
from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH
RESOURCE_PATH += 'img/'

class MouseEvents:
    def __init__(self, screen, player, original_frame, show_instructions=[False], sounds_handler=None):
        self.screen = screen
        self.player = player
        self.current_scene = self.player.current_scene
        self.original_frame = original_frame
        self.pos = [-1, -1]
        self.idling = True
        self.player_touch = None
        self.player_idling = True
        
        self.show_instructions = show_instructions
        
        if sounds_handler:
            self.sounds_handler = sounds_handler

    def set_pos(self, pos):
        x, y = (pos[1] // SCENES[self.current_scene]['cell'][0]), (pos[0] // SCENES[self.current_scene]['cell'][1])
        if [x, y] == self.pos:
            self.idling = True
            return
        self.show_instructions[0] = False
        self.idling = False
        self.pos = [x, y]

    def click(self):
        
        for key, value in SCENES[self.current_scene]['DOORS_CLICK_RANGE'].items():
            for item in value:
                if item == self.pos:
                    if self.sounds_handler and self.current_scene == 'Login':
                        self.sounds_handler.play_sfx('door_open')

                    return key, None
                
        for key, value in SCENES[self.current_scene]['OBJECTS_POS'].items():
            for item in value:
                if item == self.pos:
                    if self.sounds_handler:
                        self.sounds_handler.play_sfx('interact')
                    return None, key
                    
        return None, None

    def get_hover_frame(self, prev_frame, prev_door=None, player_touch=None):
        if player_touch:
            
            self.show_instructions[0] = False
            
            if player_touch == self.player_touch:
                return prev_frame, prev_door
            
            frame = morph_image(RESOURCE_PATH + SCENES[self.current_scene]['HOVER_FRAME'][player_touch], RESOLUTION)
            self.screen = frame.convert()
            screenCopy = self.screen.copy()
            self.player.update(screenCopy)
            
            self.player_touch = player_touch
            
            return screenCopy, player_touch
        elif self.player_touch:
            self.player_touch = None
            frame = self.original_frame
            self.screen = frame.convert()
            screenCopy = self.screen.copy()
            self.player.update(screenCopy)
            
            return screenCopy, None
        
        if self.idling:
            return prev_frame, prev_door
        door = None
        for key in SCENES[self.current_scene]['OBJECTS_POS'].keys():
            if self.pos in SCENES[self.current_scene]['OBJECTS_POS'][key]:
                door = key
                break

        if door != prev_door:
            frame = self.original_frame
            if door is not None:
                frame = morph_image(RESOURCE_PATH + SCENES[self.current_scene]['HOVER_FRAME'][door], RESOLUTION)
            self.screen = frame.convert()
            screenCopy = self.screen.copy()
            self.player.update(screenCopy)
            return screenCopy, door
        else:
            return prev_frame, door
