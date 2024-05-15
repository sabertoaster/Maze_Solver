import pygame
from CONSTANTS import RESOURCE_PATH, SOUNDS

class Sounds:
    def __init__(self, file_name, active=True):
        self.player = pygame.mixer.Sound(RESOURCE_PATH + 'sounds/' + file_name)
        self.active = active
    
    def turn_on(self):
        self.active = True  
        
    def turn_off(self):
        self.active = False
        
    def stop(self):
        self.player.stop()
        
    def _play(self, loops):
        self.player.play(loops)
        
        
class BGM(Sounds):
    def __init__(self, file_name, active=True):
        super().__init__(file_name, active=active)
                
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
        self.bgm_name = None
        self.bgm = None # class BGM 
        self.current_state = "off"
    
    def add_sfx(self, sfx_name, file_name):
        self.sfx[sfx_name] = SFX(file_name)
                
    def play_bgm(self, bgm_name):
        if self.bgm_name == bgm_name:
            return
        active = True
        if self.bgm:
            active = self.bgm.active
        pygame.mixer.stop()
        self.bgm_name = bgm_name
        self.bgm = BGM(SOUNDS['BGM'][self.bgm_name], active=active)
        self.bgm.play()
        
    def turn_on(self):
        self.current_state = "on"
        for _, sound in self.sfx.items():
            sound.turn_on()
        if self.bgm:
            self.bgm.turn_on()
                    
    def turn_off(self):
        self.current_state = "off"
        for _, sound in self.sfx.items():
            sound.turn_off()
        if self.bgm:
            self.bgm.turn_off()
                
    def switch(self):
        if self.current_state == "on":
            pygame.mixer.stop()
            self.turn_off()
        elif self.current_state == "off":
            self.turn_on()
            self.bgm.play()
        
    def play_sfx(self, sfx_name, is_transition=False):
        if is_transition:
            pygame.mixer.stop()  
        for key, s in self.sfx.items():
            if key == sfx_name:
                s.play()
                continue
            s.stop()
        
    
            
        