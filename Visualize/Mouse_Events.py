import pygame
from Visualize.ImageProcess import morph_image

SCENES = {
    'Login': {
        'OBJECTS_POS': {
            "Login" : [[x, y] for x in range(6, 10) for y in range(3, 9)],
            "Register" : [[x, y] for x in range(6, 11) for y in range(18, 27)],
            "Exit" : [[4,13]]
        },
        'HOVER_FRAME': {
            "Login": "miniTown_BG_login_hover.png",
            "Register": "miniTown_BG_register_hover.png",
            "Exit": "miniTown_BG_exit_hover.png"
        },
    },
}


class Mouse_Events:
    def __init__(self, screen, player, original_frame, PARAMS):
        self.screen = screen
        self.player = player       
        self.current_scene = self.player.current_scene
        self.original_frame = original_frame
        self.PARAMS = PARAMS
    
    def set_pos(self, pos):
        x, y = (pos[1] // self.PARAMS['cell'][0]), (pos[0] // self.PARAMS['cell'][1])
        self.pos = [x,y]
        
    def click(self):
        for key, value in SCENES[self.current_scene]['OBJECTS_POS'].items():
            for item in value:
                if item == self.pos:
                    return key
        return None
        
    def get_hover_frame(self):
        frame = self.original_frame

        for key in SCENES[self.current_scene]['OBJECTS_POS'].keys():
            if self.pos in SCENES[self.current_scene]['OBJECTS_POS'][key]:
                frame = morph_image(self.PARAMS['resources'] + SCENES[self.current_scene]['HOVER_FRAME'][key], self.PARAMS['resolution'])

        
        self.screen.blit(frame, (0, 0))
        screenCopy = self.screen.copy()
        self.player.update(screenCopy) 
           
        return screenCopy

        