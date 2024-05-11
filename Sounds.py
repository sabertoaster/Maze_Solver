import pygame
from CONSTANTS import PARAMS

class Sounds:
    def __init__(self, file_name):
        self.player = pygame.mixer.Sound(PARAMS['resources'] + 'sounds/' + file_name)
        self.active = False
    
    def turn_on(self):
        self.active = True  
    def  turn_off(self):
        self.active = False
        
class Music(Sounds):
    def __init__(self, file_name):
        super().__init__(file_name)
        
    def play(self):
        if self.active:
            self.player.play(loops=-1)

class SFX(Sounds):
    def __init__(self, file_name):
        super().__init__(file_name)
        
    def stop(self):
        self.player.stop()
        
    def play(self):
        if self.active:
            self.stop()
            self.player.play(loops=0)
        
    
            
        