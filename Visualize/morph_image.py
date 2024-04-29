import cv2
import pygame

def morph_image(target: str, resolution) -> pygame.Surface:
    result = cv2.imread(target)     # [PROTOTYPE]
    result = cv2.resize(result, resolution)
    return pygame.image.frombuffer(result.tobytes(), result.shape[1::-1], "BGR")