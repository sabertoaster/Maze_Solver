import pygame
from CONSTANTS import RESOURCE_PATH, SOUNDS

class Sounds:
    def __init__(self, file_name):
        self.player = pygame.mixer.Sound(RESOURCE_PATH + 'sounds/' + file_name)
        self.active = True
    
    def turn_on(self):
        self.active = True  
        
    def turn_off(self):
        self.active = False
        
    def stop(self):
        self.player.stop()
        
    def _play(self, loops):
        self.player.play(loops)
        
        
class BGM(Sounds):
    def __init__(self, file_name):
        super().__init__(file_name)
                
    def play(self):
        if self.active:
            self.stop()
            self._play(loops=-1)

class SFX(Sounds):
    def __init__(self, file_name):
        super().__init__(file_name)
        
    def play(self):
        if self.active:
            self.stop()
            self._play(loops=0)
            
class SoundsHandler():
    def __init__(self):
        self.sfx = dict()
        self.bgm = BGM(SOUNDS['BGM']['Login'])
        self.bgm_name = 'Login'
        self.current_state = "on"
    
    def add_sfx(self, sfx_name, file_name):
        self.sfx[sfx_name] = SFX(file_name)
                
    def play_bgm(self, file_name):
        pygame.mixer.stop()
        self.bgm = BGM(file_name)
        self.bgm_name = file_name
        self.bgm.play()
        
    def turn_on(self):
        self.current_state = "on"
        for _, sound in self.sfx.items():
            sound.turn_on()
        self.bgm.turn_on()
                    
    def turn_off(self):
        self.current_state = "off"
        for _, sound in self.sfx.items():
            sound.turn_off()
        self.bgm.turn_off()
                
    def switch(self):
        if self.current_state == "on":
            pygame.mixer.stop()
            self.turn_off()
        elif self.current_state == "off":
            self.turn_on()
            self.bgm.play()
        
    def play_sfx(self, sfx_name):
        for key, s in self.sfx.items():
            if key == sfx_name:
                s.play()
                continue
            s.stop()
        
    
            
        