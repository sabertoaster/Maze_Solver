import pygame
from Visualize.ImageProcess import morph_image
from CONSTANTS import RESOLUTION, RESOURCE_PATH
RESOURCE_PATH += 'animation/'
import os

FPS = {
    'gameplay': 24,
    'welcome': 8,
}


def play_gif(screen, original_frame=None, name='welcome'):
    """
    Play gif
    :param screen:
    :return:
    """
    frames = []
    background = original_frame
    for filename in os.listdir(RESOURCE_PATH + name):
        if filename.endswith(".png"):
            if filename == 'background.png':
                background = morph_image(RESOURCE_PATH + name + "/" + filename, RESOLUTION)
                continue
            frame = morph_image(RESOURCE_PATH + name + "/" + filename, RESOLUTION)
            frames.append(frame)
    
    num_frames = len(frames)
    
    if name == 'welcome':
        screen.blit(background, (0, 0))
        
    clock = pygame.time.Clock()

    frame = 0
    pygame.key.set_repeat()
    pygame.event.clear()
    while frame < num_frames:

        events = pygame.event.get()
        
        for event in events:
            
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                pygame.key.set_repeat(200, 125)
                return
                
        screen.blit(frames[frame], (0, 0))
        pygame.display.flip()
        screen.blit(background, (0, 0))
        
        frame += 1
        
        if name == 'welcome':
            if frame == num_frames:
                frame = 0
                
        clock.tick(FPS[name])
    pygame.key.set_repeat(200, 125)