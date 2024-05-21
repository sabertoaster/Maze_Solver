import pygame
from Visualize.ImageProcess import morph_image
from CONSTANTS import RESOLUTION, SCENES, RESOURCE_PATH


class MouseEvents:
    def __init__(self, screen, player, original_frame):
        self.screen = screen
        self.player = player
        self.current_scene = self.player.current_scene
        self.original_frame = original_frame
        self.pos = [-1, -1]
        self.idling = True

    def set_pos(self, pos):
        x, y = (pos[1] // SCENES[self.current_scene]['cell'][0]), (pos[0] // SCENES[self.current_scene]['cell'][1])
        if [x, y] == self.pos:
            self.idling = True
            return
        self.idling = False
        self.pos = [x, y]

    def click(self):
        print(self.current_scene)
        
        for key, value in SCENES[self.current_scene]['DOORS_CLICK_RANGE'].items():
            for item in value:
                if item == self.pos:
                    return key, None
                
        for key, value in SCENES[self.current_scene]['OBJECTS_POS'].items():
            for item in value:
                if item == self.pos:
                    return None, key
                    
                
        return None, None

    def get_hover_frame(self, prev_frame, prev_obj=None):
        print('self.player.touched_obj:: ', self.player.touched_obj)
        if self.player.touched_obj:
            if self.player.touched_obj != prev_obj:
                frame = morph_image(RESOURCE_PATH + SCENES[self.current_scene]['HOVER_FRAME'][self.player.touched_obj], RESOLUTION)
                self.screen = frame.convert()
                screenCopy = self.screen.copy()
                self.player.update(screenCopy)
                                
                return screenCopy, self.player.touched_obj
            else:
                return prev_frame, prev_obj 

        obj = None
        if not self.player.touched_obj:
            for key in SCENES[self.current_scene]['OBJECTS_POS'].keys():
                if self.pos in SCENES[self.current_scene]['OBJECTS_POS'][key]:
                    obj = key
                    break
            
        if self.idling:
            if not self.player.touched_obj and prev_obj and not obj:
                self.screen = self.original_frame
                screenCopy = self.screen.copy()
                self.player.update(screenCopy)
                self.player_touching_prev = None
                return screenCopy, None
            # if not self.player_touching and obj:
            #     frame = morph_image(RESOURCE_PATH + SCENES[self.current_scene]['HOVER_FRAME'][obj], RESOLUTION)
            #     self.screen = frame.convert()
            #     screenCopy = self.screen.copy()
            #     self.player.update(screenCopy)
            #     return screenCopy, obj
            return prev_frame, prev_obj
        
                 
        if obj != prev_obj:
            frame = self.original_frame
            if obj:
                frame = morph_image(RESOURCE_PATH + SCENES[self.current_scene]['HOVER_FRAME'][obj], RESOLUTION)
            self.screen = frame.convert()
            screenCopy = self.screen.copy()
            self.player.update(screenCopy)
            return screenCopy, obj
        else:
            return prev_frame, obj
